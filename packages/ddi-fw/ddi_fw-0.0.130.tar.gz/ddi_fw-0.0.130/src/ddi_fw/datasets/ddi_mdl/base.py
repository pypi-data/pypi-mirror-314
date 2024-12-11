import pathlib

import numpy as np
import pandas as pd

from ddi_fw.datasets.feature_vector_generation import SimilarityMatrixGenerator
from ddi_fw.langchain.embeddings import PoolingStrategy
from .. import BaseDataset
from ..db_utils import create_connection

HERE = pathlib.Path(__file__).resolve().parent
list_of_embedding_columns = ['all_text', 'description',
                     'synthesis_reference', 'indication',
                     'pharmacodynamics', 'mechanism_of_action',
                     'toxicity', 'metabolism',
                     'absorption', 'half_life',
                     'protein_binding', 'route_of_elimination',
                     'volume_of_distribution', 'clearance']

list_of_chemical_property_columns = ['enzyme',
                             'target',
                             'pathway',
                             'smile']
list_of_ner_columns = ['tui', 'cui', 'entities']


def indices_to_binary_vector(indices, vector_length=881):
    # vector_length = len(indices)
    # Initialize a zero vector of the given length
    binary_vector = [0] * vector_length
    
    # Set the positions specified by indices to 1
    for index in indices:
        if 0 <= index < vector_length:
            binary_vector[index] = 1
    
    return binary_vector

class DDIMDLDataset(BaseDataset):
    def __init__(self, embedding_size,
                 embedding_dict,
                 embeddings_pooling_strategy: PoolingStrategy,
                 ner_df,
                 chemical_property_columns=['enzyme',
                                            'target',
                                            'pathway',
                                            'smile'],
                 embedding_columns=[],
                 ner_columns=[],
                 **kwargs):
        columns = kwargs['columns']
        if columns:
            chemical_property_columns = []
            embedding_columns=[]
            ner_columns=[]
            for column in columns:
                if column in list_of_chemical_property_columns:
                    chemical_property_columns.append(column)
                elif column in list_of_embedding_columns:
                    embedding_columns.append(column)
                elif column in list_of_ner_columns:
                    ner_columns.append(column)
                # elif column == 'smile_2':
                #     continue
                else:
                    raise Exception(f"{column} is not related this dataset")


        super().__init__(embedding_size=embedding_size,
                         embedding_dict=embedding_dict,
                         embeddings_pooling_strategy=embeddings_pooling_strategy,
                         ner_df=ner_df,
                         chemical_property_columns=chemical_property_columns,
                         embedding_columns=embedding_columns,
                         ner_columns=ner_columns,
                         **kwargs)

        # kwargs = {'index_path': str(HERE.joinpath('indexes'))}
        kwargs['index_path'] = str(HERE.joinpath('indexes'))

        db = HERE.joinpath('data/event.db')
        conn = create_connection(db)
        print("db prep")
        self.drugs_df = self.__select_all_drugs_as_dataframe__(conn)
        self.ddis_df = self.__select_all_events__(conn)
        print("db bitti")
        self.index_path = kwargs.get('index_path')

        # jaccard_sim_dict = {}
        # sim_matrix_gen = SimilarityMatrixGenerator()
        # jaccard_sim_dict["smile_2"] = sim_matrix_gen.create_jaccard_similarity_matrices(
        #                 self.drugs_df["smile_2"].to_list())
        
        # similarity_matrices = {}
        # drugbank_ids = self.drugs_df['id'].to_list()
        # new_columns = {}
        # for idx in range(len(drugbank_ids)):
        #     new_columns[idx] = drugbank_ids[idx]
        # new_df = pd.DataFrame.from_dict(jaccard_sim_dict["smile_2"])
        # new_df = new_df.rename(index=new_columns, columns=new_columns)
        # similarity_matrices["smile_2"] = new_df
        
        
        # def lambda_fnc(row, value):
        #     if row['id1'] in value and row['id2'] in value:
        #         return np.float16(np.hstack(
        #             (value[row['id1']], value[row['id2']])))
        # for key, value in similarity_matrices.items():

        #     print(f'sim matrix: {key}')
        #     self.ddis_df[key] = self.ddis_df.apply(
        #         lambda_fnc, args=(value,), axis=1)
        #     print(self.ddis_df[key].head())
        # print("init finished")

    def __select_all_drugs_as_dataframe__(self, conn):
        headers = ['index', 'id', 'name',
                   'target', 'enzyme', 'pathway', 'smile']
        cur = conn.cursor()
        cur.execute(
            '''select "index", id, name, target, enzyme, pathway, smile from drug''')
        rows = cur.fetchall()
        df = pd.DataFrame(columns=headers, data=rows)
        df['enzyme'] = df['enzyme'].apply(lambda x: x.split('|'))
        df['target'] = df['target'].apply(lambda x: x.split('|'))
        df['pathway'] = df['pathway'].apply(lambda x: x.split('|'))
        # df['smile_2'] = df['smile'].apply(lambda x: indices_to_binary_vector(indices = list(map(int, x.split('|'))), vector_length = 881))
        df['smile'] = df['smile'].apply(lambda x: x.split('|'))
        
            
        return df

    def __select_all_events__(self, conn):
        """
        Query all rows in the event table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute('''
                select ex."index", d1.id, d1.name, d2.id, d2.name,  mechanism || ' ' ||action from extraction ex
                join drug d1 on  d1.name = ex.drugA
                join drug d2 on  d2.name = ex.drugB
        ''')

        rows = cur.fetchall()

        headers = ["index", "id1", "name1", "id2", "name2", "event_category"]
        return pd.DataFrame(columns=headers, data=rows)
