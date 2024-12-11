import glob
from sklearn.model_selection import KFold, StratifiedKFold, train_test_split
from sklearn.preprocessing import LabelBinarizer
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import pathlib
from ddi_fw.langchain.embeddings import PoolingStrategy
from ddi_fw.datasets.idf_helper import IDF

from ddi_fw.utils.zip_helper import ZipHelper
from .feature_vector_generation import SimilarityMatrixGenerator, VectorGenerator
# from ddi_fw.ner.ner import CTakesNER
from ddi_fw.utils import create_folder_if_not_exists
from stopwatch import Stopwatch, profile

HERE = pathlib.Path(__file__).resolve().parent


def stack(df_column):
    return np.stack(df_column.values)


class BaseDataset(ABC):
    def __init__(self,
                 embedding_size,
                 embedding_dict,
                 embeddings_pooling_strategy: PoolingStrategy,
                 ner_df,
                 chemical_property_columns,
                 embedding_columns,
                 ner_columns,
                 **kwargs):
        self.embedding_size = embedding_size
        self.embedding_dict = embedding_dict
        self.embeddings_pooling_strategy = embeddings_pooling_strategy
        self.ner_df = ner_df
        self.__similarity_related_columns__ = []
        self.__similarity_related_columns__.extend(chemical_property_columns)
        self.__similarity_related_columns__.extend(ner_columns)

        self.chemical_property_columns = chemical_property_columns
        self.embedding_columns = embedding_columns
        self.ner_columns = ner_columns
        self.threshold_method = kwargs.get('threshold_method', 'idf')
        self.tui_threshold = kwargs.get('tui_threshold', 0)
        self.cui_threshold = kwargs.get('cui_threshold', 0)
        self.entities_threshold = kwargs.get('entities_threshold', 0)

        self.stopwatch = Stopwatch()

        # self.store_similarity_matrices = kwargs.get('store_similarity_matrices', True)
        # self.similarity_matrices_path = kwargs.get('similarity_matrices_path', True)

# önce load veya split çalıştırılmalı
    def produce_inputs(self):
        items = []
        y_train_label, y_test_label = stack(self.y_train), stack(self.y_test)
        # self.__similarity_related_columns__.append("smile_2") #TODO
        for column in self.__similarity_related_columns__:
            train_data, test_data = stack(
                self.X_train[column]), stack(self.X_test[column])
            items.append([f'{column}', np.nan_to_num(train_data),
                          y_train_label, np.nan_to_num(test_data), y_test_label])
        for column in self.embedding_columns:
            train_data, test_data = stack(
                self.X_train[column+'_embedding']), stack(self.X_test[column+'_embedding'])
            items.append([f'{column}_embedding', train_data,
                          y_train_label, test_data, y_test_label])
        return items

# remove this function
    def generate_sim_matrices(self, chemical_properties_df, two_d_dict):

        jaccard_sim_dict = {}
        sim_matrix_gen = SimilarityMatrixGenerator()

        for column in self.__similarity_related_columns__:
            key = '2D_'+column
            jaccard_sim_dict[column] = sim_matrix_gen.create_jaccard_similarity_matrices(
                two_d_dict[key])

        drugbank_ids = chemical_properties_df['id'].to_list()

        similarity_matrices = {}

        for column in self.__similarity_related_columns__:
            sim_matrix = jaccard_sim_dict[column]
            jaccard_sim_feature = {}
            for i in range(len(drugbank_ids)):
                jaccard_sim_feature[drugbank_ids[i]] = sim_matrix[i]
            similarity_matrices[column] = jaccard_sim_feature

        return similarity_matrices

    def generate_sim_matrices_new(self, chemical_properties_df):
        self.stopwatch.reset()
        self.stopwatch.start()
        jaccard_sim_dict = {}
        sim_matrix_gen = SimilarityMatrixGenerator()

        for column in self.__similarity_related_columns__:
            # key = '2D_'+column
            key = column
            jaccard_sim_dict[column] = sim_matrix_gen.create_jaccard_similarity_matrices(
                self.generated_vectors[key])
        self.stopwatch.stop()
        print(f'similarity_matrix_generation_part_1: {self.stopwatch.elapsed}')

        self.stopwatch.reset()
        self.stopwatch.start()
        similarity_matrices = {}
        drugbank_ids = chemical_properties_df['id'].to_list()
        new_columns = {}
        for idx in range(len(drugbank_ids)):
            new_columns[idx] = drugbank_ids[idx]
        for column in self.__similarity_related_columns__:
            new_df = pd.DataFrame.from_dict(jaccard_sim_dict[column])
            new_df = new_df.rename(index=new_columns, columns=new_columns)
            similarity_matrices[column] = new_df
        self.stopwatch.stop()
        print(f'similarity_matrix_generation_part_2: {self.stopwatch.elapsed}')
        return similarity_matrices

    # matris formuna çevirmek için
    def transform_2d(self, chemical_properties_df):
        two_d_dict = {}
        for column in self.__similarity_related_columns__:
            key = '2D_'+column
            new_column = column + '_vectors'
            two_d_dict[key] = np.stack(
                chemical_properties_df[new_column].to_numpy())

        return two_d_dict

    # todo dictionary içinde ndarray dönsün
    def generate_vectors(self, chemical_properties_df):
        self.stopwatch.reset()
        self.stopwatch.start()
        vectorGenerator = VectorGenerator(chemical_properties_df)

        new_columns = [
            c+'_vectors' for c in self.__similarity_related_columns__]
        self.generated_vectors = vectorGenerator.generate_feature_vectors(
            self.__similarity_related_columns__)

        # for column, new_column in zip(self.__similarity_related_columns__, new_columns):
        #     chemical_properties_df.loc[:,
        #                                new_column] = generated_vectors[column]
        # self.generated_vectors = generated_vectors
        self.stopwatch.stop()
        print(f'vector_generation: {self.stopwatch.elapsed}')


# remove this function


    def sim(self, chemical_properties_df):
        self.stopwatch.reset()
        self.stopwatch.start()
        from scipy.spatial.distance import pdist
        sim_matrix_gen = SimilarityMatrixGenerator()

        drugbank_ids = chemical_properties_df['id'].to_list()
        similarity_matrices = {}
        for column in self.__similarity_related_columns__:
            df = pd.DataFrame(np.stack(
                chemical_properties_df[f'{column}_vectors'].values), index=drugbank_ids)
        #   similarity_matrices[column] = 1 - pdist(df.to_numpy(), metric='jaccard')
            similarity_matrices[column] = sim_matrix_gen.create_jaccard_similarity_matrices(
                df.to_numpy())
        self.stopwatch.stop()
        print(f'sim: {self.stopwatch.elapsed}')
        return similarity_matrices

# import pandas as pd
# a = [[0,0,1],[0,0,1],[0,0,0]]
# s = pd.Series(a)
# # print(np.vstack(s.to_numpy()))
# l = np.argmax(np.vstack(s.to_numpy()),axis = 1)
# l
    def split_dataset(self,
                      fold_size=5,
                      shuffle=True,
                      test_size=0.2,
                      save_indexes=False):
        save_path = self.index_path
        self.prep()
        X = self.dataframe.drop('class', axis=1)
        y = self.dataframe['class']
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, shuffle=shuffle, test_size=test_size, stratify=np.argmax(np.vstack(y.to_numpy()), axis=1))
        # k_fold = KFold(n_splits=fold_size, shuffle=shuffle, random_state=1)
        # folds = k_fold.split(X_train)

        k_fold = StratifiedKFold(
            n_splits=fold_size, shuffle=shuffle, random_state=1)
        folds = k_fold.split(X_train, np.argmax(
            np.vstack(y_train.to_numpy()), axis=1))
        train_idx_arr = []
        val_idx_arr = []
        for i, (train_index, val_index) in enumerate(folds):
            train_idx_arr.append(train_index)
            val_idx_arr.append(val_index)

        if save_indexes:
            # train_pairs = [row['id1'].join(',').row['id2'] for index, row in X_train.iterrows()]
            self.__save_indexes__(
                save_path, 'train_indexes.txt', X_train['index'].values)
            self.__save_indexes__(
                save_path, 'test_indexes.txt',  X_test['index'].values)
            # self.__save_indexes__(
            #     save_path, 'train_indexes.txt', X_train.index.values)
            # self.__save_indexes__(
            #     save_path, 'test_indexes.txt',  X_test.index.values)

            for i, (train_idx, val_idx) in enumerate(zip(train_idx_arr, val_idx_arr)):
                self.__save_indexes__(
                    save_path, f'train_fold_{i}.txt', train_idx)
                self.__save_indexes__(
                    save_path, f'validation_fold_{i}.txt', val_idx)

        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.train_indexes = X_train.index
        self.test_indexes = X_test.index
        self.train_idx_arr = train_idx_arr
        self.val_idx_arr = val_idx_arr
        return X_train, X_test, y_train, y_test, X_train.index, X_test.index, train_idx_arr, val_idx_arr

    def __get_indexes__(self, path):
        train_index_path = path+'/train_indexes.txt'
        test_index_path = path+'/test_indexes.txt'
        train_fold_files = f'{path}/train_fold_*.txt'
        val_fold_files = f'{path}/validation_fold_*.txt'
        train_idx_arr = []
        val_idx_arr = []
        with open(train_index_path, 'r', encoding="utf8") as f:
            train_idx_all = [int(r) for r in f.readlines()]
        with open(test_index_path, 'r', encoding="utf8") as f:
            test_idx_all = [int(r) for r in f.readlines()]

        for filepath in glob.glob(train_fold_files):
            with open(filepath, 'r', encoding="utf8") as f:
                train_idx = [int(r) for r in f.readlines()]
                train_idx_arr.append(train_idx)
        for filepath in glob.glob(val_fold_files):
            with open(filepath, 'r', encoding="utf8") as f:
                val_idx = [int(r) for r in f.readlines()]
                val_idx_arr.append(val_idx)
        return train_idx_all, test_idx_all, train_idx_arr, val_idx_arr

    def __save_indexes__(self, path, filename, indexes):
        create_folder_if_not_exists(path)
        file_path = path + '/'+filename
        str_indexes = [str(index) for index in indexes]
        with open(file_path, 'w') as f:
            f.write('\n'.join(str_indexes))

    # @abstractmethod
    # def prep(self):
    #     pass

    # @abstractmethod
    # def load(self):
    #     pass

# her bir metin tipi için embedding oluşturursan burayı düzenle
    def prep(self):
        drug_names = self.drugs_df['name'].to_list()
        drug_ids = self.drugs_df['id'].to_list()

        filtered_df = self.drugs_df
        combined_df = filtered_df.copy()

        if self.ner_df is not None and not self.ner_df.empty:
            filtered_ner_df = self.ner_df[self.ner_df['drugbank_id'].isin(
                drug_ids)]
            filtered_ner_df = self.ner_df.copy()

            # TODO: eğer kullanılan veri setinde tui, cui veya entity bilgileri yoksa o veri setine bu sütunları eklemek için aşağısı gerekli

            # idf_calc = IDF(filtered_ner_df, [f for f in filtered_ner_df.keys()])
            idf_calc = IDF(filtered_ner_df, self.ner_columns)
            idf_calc.calculate()
            idf_scores_df = idf_calc.to_dataframe()

            # for key in filtered_ner_df.keys():
            for key in self.ner_columns:
                threshold = 0
                if key.startswith('tui'):
                    threshold = self.tui_threshold
                if key.startswith('cui'):
                    threshold = self.cui_threshold
                if key.startswith('entities'):
                    threshold = self.entities_threshold
                combined_df[key] = filtered_ner_df[key]
                valid_codes = idf_scores_df[idf_scores_df[key] > threshold].index

                # print(f'{key}: valid code size = {len(valid_codes)}')
                combined_df[key] = combined_df[key].apply(lambda items:
                                                        [item for item in items if item in valid_codes])

        moved_columns = ['id']
        moved_columns.extend(self.__similarity_related_columns__)
        chemical_properties_df = combined_df[moved_columns]

        chemical_properties_df = chemical_properties_df.fillna("").apply(list)

        # generate vectors dictionary içinde ndarray dönecek
        self.generate_vectors(chemical_properties_df)

        # two_d_dict = self.transform_2d(chemical_properties_df)

        similarity_matrices = self.generate_sim_matrices_new(
            chemical_properties_df)

        # similarity_matrices = self.sim(chemical_properties_df)

        event_categories = self.ddis_df['event_category']
        labels = event_categories.tolist()
        lb = LabelBinarizer()
        lb.fit(labels)
        classes = lb.transform(labels)

        # def similarity_lambda_fnc(row, value):
        #     if row['id1'] in value and row['id2'] in value:
        #         return value[row['id1']][row['id2']]

        def similarity_lambda_fnc(row, value):
            if row['id1'] in value:
                return value[row['id1']]

        def lambda_fnc(row, value):
            if row['id1'] in value and row['id2'] in value:
                return np.float16(np.hstack(
                    (value[row['id1']], value[row['id2']])))
                # return np.hstack(
                #     (value[row['id1']], value[row['id2']]), dtype=np.float16)

        def x_fnc(row, embeddings_after_pooling):
            if row['id1'] in embeddings_after_pooling:
                v1 = embeddings_after_pooling[row['id1']]
            else:
                v1 = np.zeros(self.embedding_size)
            if row['id2'] in embeddings_after_pooling:
                v2 = embeddings_after_pooling[row['id2']]
            else:
                v2 = np.zeros(self.embedding_size)
            return np.float16(np.hstack(
                (v1, v2)))

        for key, value in similarity_matrices.items():

            print(f'sim matrix: {key}')
            self.ddis_df[key] = self.ddis_df.apply(
                lambda_fnc, args=(value,), axis=1)
            print(self.ddis_df[key].head())

        for embedding_column in self.embedding_columns:
            print(f"concat {embedding_column} embeddings")
            embeddings_after_pooling = {k: self.embeddings_pooling_strategy.apply(
                v) for k, v in self.embedding_dict[embedding_column].items()}
            # column_embeddings_dict = embedding_values[embedding_column]
            self.ddis_df[embedding_column+'_embedding'] = self.ddis_df.apply(
                x_fnc, args=(embeddings_after_pooling,), axis=1)

        self.dataframe = self.ddis_df.copy()
        self.dataframe['class'] = list(classes)
        print(self.dataframe.shape)

    def load(self):
        if self.index_path == None:
            raise Exception(
                "There is no index path, please call split function")

        # prep - split - load
        train_idx_all, test_idx_all, train_idx_arr, val_idx_arr = self.__get_indexes__(
            self.index_path)

        self.prep()
        train = self.dataframe[self.dataframe['index'].isin(train_idx_all)]
        test = self.dataframe[self.dataframe['index'].isin(test_idx_all)]

        self.X_train = train.drop('class', axis=1)
        self.y_train = train['class']
        self.X_test = test.drop('class', axis=1)
        self.y_test = test['class']

        self.train_indexes = self.X_train.index
        self.test_indexes = self.X_test.index
        self.train_idx_arr = train_idx_arr
        self.val_idx_arr = val_idx_arr

        return self.X_train, self.X_test, self.y_train, self.y_test, self.X_train.index, self.X_test.index, train_idx_arr, val_idx_arr

        def export_as_csv(self, output_file_path, not_change: list):
            copy = self.dataframe.copy()
            for col in copy.columns:
                if col not in not_change:
                    copy[col] = [
                        '[' + ','.join(f"{value:.3f}" for value in row) + ']' for row in copy[col]]
            copy.to_csv(output_file_path, index=False)
