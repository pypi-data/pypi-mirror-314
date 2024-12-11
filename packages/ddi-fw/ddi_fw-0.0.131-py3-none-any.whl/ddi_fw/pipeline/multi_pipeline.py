import json
from ddi_fw.pipeline.pipeline import Pipeline
from ddi_fw.pipeline.ner_pipeline import NerParameterSearch
import importlib


def load_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config


def get_import(full_path_of_import):
    """Dynamically imports an object from a module given its full path.

    Args:
        full_path_of_import (str): The full path of the import (e.g., 'module.submodule.ClassName').

    Returns:
        object: The imported object.

    Raises:
        ImportError: If the module cannot be imported.
        AttributeError: If the attribute does not exist in the module.
    """
    if not full_path_of_import:
        raise ValueError("The import path cannot be empty.")

    parts = full_path_of_import.split('.')
    import_name = parts[-1]
    module_name = ".".join(parts[:-1]) if len(parts) > 1 else ""

    try:
        module = importlib.import_module(module_name)
        return getattr(module, import_name)
    except ModuleNotFoundError as e:
        raise ImportError(f"Module '{module_name}' could not be found.") from e
    except AttributeError as e:
        raise AttributeError(
            f"'{module_name}' has no attribute '{import_name}'") from e


class MultiPipeline():
    def __init__(self, experiments_config_file):
        self.experiments_config = load_config(experiments_config_file)
        self.items = []
        self.pipeline_resuts = dict()

    def __create_pipeline(self, config):
        type = config.get("type")
        library = config.get("library")
        batch_size = config.get("batch_size")
        epochs = config.get("epochs")

        # dataset_module = config.get("dataset_module")
        # dataset_name = config.get("dataset_name")

        experiment_name = config.get("experiment_name")
        experiment_description = config.get("experiment_description")
        experiment_tags = config.get("experiment_tags")
        tracking_uri = config.get("tracking_uri")
        artifact_location = config.get("artifact_location")
        columns = config.get("columns")
        ner_data_file = config.get("ner_data_file")
        ner_threshold = config.get("ner_threshold")
        column_embedding_configs = config.get("column_embedding_configs")
        vector_db_persist_directory = config.get("vector_db_persist_directory")
        vector_db_collection_name = config.get("vector_db_collection_name")
        embedding_pooling_strategy = get_import(
            config.get("embedding_pooling_strategy_type")) if config.get("embedding_pooling_strategy_type") else None
        # Dynamically import the model and dataset classes
        model_type = get_import(config.get("model_type"))
        dataset_type = get_import(config.get("dataset_type"))
        combination_type = None
        kwargs_combination_params=None
        if config.get("combination_strategy"):
            combination_type = get_import(config.get("combination_strategy").get("type"))
            kwargs_combination_params = config.get("combination_strategy").get("params")
        combinations = []
        if combination_type is not None:
            combinations = combination_type(**kwargs_combination_params).generate()
        # # Instantiate the classes
        # model_instance = model_class()
        # dataset_instance = dataset_class()

        pipeline = None
        if type == "general":
            pipeline = Pipeline(
                library=library,
                experiment_name=experiment_name,
                experiment_description=experiment_description,
                experiment_tags=experiment_tags,
                artifact_location=artifact_location,
                tracking_uri=tracking_uri,
                dataset_type=dataset_type,
                columns=columns,
                column_embedding_configs=column_embedding_configs,
                vector_db_persist_directory=vector_db_persist_directory,
                vector_db_collection_name=vector_db_collection_name,
                embedding_pooling_strategy_type=embedding_pooling_strategy,
                ner_data_file=ner_data_file,
                ner_threshold=ner_threshold,
                combinations=combinations)
        elif type== "ner_search":
            pipeline = NerParameterSearch(
                library=library,
                experiment_name=experiment_name,
                experiment_description=experiment_description,
                experiment_tags=experiment_tags,
                tracking_uri=tracking_uri,
                dataset_type=dataset_type,
                umls_code_types = None,
                text_types = None,
                columns=['tui', 'cui', 'entities'],
                ner_data_file=ner_data_file,
            )


        return {
            "name": experiment_name,
            "library": library,
            "batch_size": batch_size,
            "epochs": epochs,
            "model_type": model_type,
            "pipeline": pipeline}

    def build(self):
        for config in self.experiments_config['experiments']:
            item = self.__create_pipeline(config)
            self.items.append(item)
        return self

    def run(self):
        for item in self.items:
            print(f"{item['name']} is running")
            pipeline = item['pipeline']
            model_type = item['model_type']
            batch_size = item['batch_size']
            epochs = item['epochs']
            # It can be moved to build function
            pipeline.build()
            result = pipeline.run(model_type, epochs=epochs, batch_size=batch_size)
            self.pipeline_resuts[item['name']] = result
        return self

    def results(self):
        return self.pipeline_resuts