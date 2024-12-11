import numpy as np
import pandas as pd
import chromadb
from collections import defaultdict
from ddi_fw.ner.ner import CTakesNER
from ddi_fw.langchain.embeddings import PoolingStrategy
from ddi_fw.datasets import BaseDataset, DDIMDLDataset
from ddi_fw.langchain.embeddings import SumPoolingStrategy
import mlflow
from ddi_fw.ml import MultiModalRunner


class Pipeline:
    def __init__(self,
                 library='tensorflow',
                 experiment_name=None,
                 experiment_description=None,
                 experiment_tags=None,
                 artifact_location=None,
                 tracking_uri=None,
                 dataset_type: BaseDataset = None,
                 columns=None,
                 embedding_dict=None,
                 column_embedding_configs=None,
                 vector_db_persist_directory=None,
                 vector_db_collection_name=None,
                 embedding_pooling_strategy_type: PoolingStrategy = None,
                 ner_data_file=None,
                 ner_threshold=None,
                 combinations=None,
                 model=None):
        self.library = library
        self.experiment_name = experiment_name
        self.experiment_description = experiment_description
        self.experiment_tags = experiment_tags
        self.artifact_location = artifact_location
        self.tracking_uri = tracking_uri
        self.dataset_type = dataset_type
        self.columns = columns
        self.embedding_dict = embedding_dict
        self.column_embedding_configs = column_embedding_configs
        self.vector_db_persist_directory = vector_db_persist_directory
        self.vector_db_collection_name = vector_db_collection_name
        self.embedding_pooling_strategy_type = embedding_pooling_strategy_type
        self.ner_data_file = ner_data_file
        self.ner_threshold = ner_threshold
        self.combinations = combinations
        self.model = model

    def __create_or_update_embeddings__(self, embedding_dict, vector_db_persist_directory, vector_db_collection_name, column=None):
        """
        Fetch embeddings and metadata from a persistent Chroma vector database and update the provided embedding_dict.

        Args:
        - vector_db_persist_directory (str): The path to the directory where the Chroma vector database is stored.
        - vector_db_collection_name (str): The name of the collection to query.
        - embedding_dict (dict): The existing dictionary to update with embeddings.

        """
        if vector_db_persist_directory:
            # Initialize the Chroma client and get the collection
            vector_db = chromadb.PersistentClient(
                path=vector_db_persist_directory)
            collection = vector_db.get_collection(vector_db_collection_name)

            # Fetch the embeddings and metadata
            if column == None:
                dictionary = collection.get(
                    include=['embeddings', 'metadatas'])
                print(
                    f"Embeddings are calculated from {vector_db_collection_name}")
            else:
                dictionary = collection.get(include=['embeddings', 'metadatas'], where={
                                            "type": {"$eq": f"{column}"}})
                print(
                    f"Embeddings of {column} are calculated from {vector_db_collection_name}")
            # Populate the embedding dictionary with embeddings from the vector database
            for metadata, embedding in zip(dictionary['metadatas'], dictionary['embeddings']):
                embedding_dict[metadata["type"]
                               ][metadata["id"]].append(embedding)

            # return dictionary['embeddings'].shape[1]
        else:
            raise ValueError(
                "Persistent directory for the vector DB is not specified.")

    def build(self):
        # 'enzyme','target','pathway','smile','all_text','indication', 'description','mechanism_of_action','pharmacodynamics', 'tui', 'cui', 'entities'
        kwargs = {"columns": self.columns}
        if self.ner_threshold:
            for k, v in self.ner_threshold.items():
                kwargs[k] = v
        if self.embedding_dict == None:
            embedding_dict = defaultdict(lambda: defaultdict(list))
            # TODO find more effective solution

            if self.column_embedding_configs:
                for item in self.column_embedding_configs:
                    col = item["column"]
                    col_db_dir = item["vector_db_persist_directory"]
                    col_db_collection = item["vector_db_collection_name"]
                    self.__create_or_update_embeddings__(
                        embedding_dict, col_db_dir, col_db_collection, col)
                    
            elif self.vector_db_persist_directory:
                self.__create_or_update_embeddings__(
                    embedding_dict, self.vector_db_persist_directory, self.vector_db_collection_name)
                
            else:
                print(
                    f"There is no configuration of Embeddings")

        # if self.embedding_dict == None:
        #     if self.vector_db_persist_directory:
        #         self.vector_db = chromadb.PersistentClient(
        #             path=self.vector_db_persist_directory)
        #         self.collection = self.vector_db.get_collection(
        #             self.vector_db_collection_name)
        #         dictionary = self.collection.get(
        #             include=['embeddings', 'metadatas'])

        #         embedding_dict = defaultdict(lambda: defaultdict(list))

        #         for metadata, embedding in zip(dictionary['metadatas'], dictionary['embeddings']):
        #             embedding_dict[metadata["type"]
        #                            ][metadata["id"]].append(embedding)

        #         embedding_size = dictionary['embeddings'].shape[1]
        else:
            embedding_dict = self.embedding_dict
            # TODO make generic
            # embedding_size = list(embedding_dict['all_text'].values())[
            #     0][0].shape
        key, value = next(iter(embedding_dict.items()))
        embedding_size = value[next(iter(value))][0].shape[0]
        pooling_strategy = self.embedding_pooling_strategy_type()

        self.ner_df = CTakesNER().load(
            filename=self.ner_data_file) if self.ner_data_file else None

        self.dataset = self.dataset_type(
            embedding_dict=embedding_dict,
            embedding_size=embedding_size,
            embeddings_pooling_strategy=pooling_strategy,
            ner_df=self.ner_df, **kwargs)

        X_train, X_test, y_train, y_test, X_train.index, X_test.index, train_idx_arr, val_idx_arr = self.dataset.load()

        self.dataframe = self.dataset.dataframe
        # dataframe.dropna()
        self.X_train = self.dataset.X_train
        self.X_test = self.dataset.X_test
        self.y_train = self.dataset.y_train
        self.y_test = self.dataset.y_test
        self.train_idx_arr = self.dataset.train_idx_arr
        self.val_idx_arr = self.dataset.val_idx_arr
        # Logic to set up the experiment
        self.items = self.dataset.produce_inputs()

        unique_classes = pd.unique(self.dataframe['event_category'])
        event_num = len(unique_classes)
        # droprate = 0.3
        vector_size = self.dataset.drugs_df.shape[0]

        print("Building the experiment with the following settings:")
        print(
            f"Name: {self.experiment_name}, Dataset: {self.dataset}, Model: {self.model}")
        # Implement additional build logic as needed
        return self

    def run(self, model_func, batch_size=128, epochs=100):
        mlflow.set_tracking_uri(self.tracking_uri)

        if mlflow.get_experiment_by_name(self.experiment_name) == None:
            mlflow.create_experiment(
                self.experiment_name, self.artifact_location)
            mlflow.set_experiment_tags(self.experiment_tags)
        mlflow.set_experiment(self.experiment_name)

        y_test_label = self.items[0][4]
        multi_modal_runner = MultiModalRunner(
            library=self.library, model_func=model_func, batch_size=batch_size,  epochs=epochs)
        # multi_modal = TFMultiModal(
        #     model_func=model_func, batch_size=batch_size,  epochs=epochs)  # 100
        multi_modal_runner.set_data(
            self.items, self.train_idx_arr, self.val_idx_arr, y_test_label)
        result = multi_modal_runner.predict(self.combinations)
        return result
