import os
import pathlib
import sqlite3
from sqlite3 import Error
import pandas as pd

from ddi_fw.utils import ZipHelper

from ..core import BaseDataset
# from ..db_utils import create_connection, select_all_drugs_as_dataframe, select_events_with_category

HERE = pathlib.Path(__file__).resolve().parent


class MDFSADDIDataset(BaseDataset):
    def __init__(self, chemical_property_columns=['enzyme',
                                                  'target',
                                                  'smile'],
                 embedding_columns=[],
                 ner_columns=[],
                 **kwargs):

        super().__init__(chemical_property_columns, embedding_columns,
                         ner_columns, **kwargs)

        db_zip_path = HERE.joinpath('mdf-sa-ddi.zip')
        db_path = HERE.joinpath('mdf-sa-ddi.db')
        if not os.path.exists(db_zip_path):
            self.__to_db__(db_path)
        else:
            ZipHelper().extract(
                input_path=str(HERE), output_path=str(HERE))
            conn = create_connection(db_path)
            self.drugs_df = select_all_drugs_as_dataframe(conn)
            self.ddis_df = select_all_events_as_dataframe(conn)
        kwargs = {'index_path': str(HERE.joinpath('indexes'))}

        self.index_path = kwargs.get('index_path')

    def __to_db__(self, db_path):
        conn = create_connection(db_path)
        drugs_path = HERE.joinpath('drug_information_del_noDDIxiaoyu50.csv')
        ddis_path = HERE.joinpath('df_extraction_cleanxiaoyu50.csv')
        self.drugs_df = pd.read_csv(drugs_path)
        self.ddis_df = pd.read_csv(ddis_path)
        self.drugs_df.drop(columns="Unnamed: 0", inplace=True)
        self.ddis_df.drop(columns="Unnamed: 0", inplace=True)

        self.ddis_df.rename(
            columns={"drugA": "name1", "drugB": "name2"}, inplace=True)
        self.ddis_df['event_category'] = self.ddis_df['mechanism'] + \
            ' ' + self.ddis_df['action']

        reverse_ddis_df = pd.DataFrame()
        reverse_ddis_df['id1'] = self.ddis_df['id2']
        reverse_ddis_df['name1'] = self.ddis_df['name2']
        reverse_ddis_df['id2'] = self.ddis_df['id1']
        reverse_ddis_df['name2'] = self.ddis_df['name1']
        reverse_ddis_df['event_category'] = self.ddis_df['event_category']

        self.ddis_df = pd.concat(
            [self.ddis_df, reverse_ddis_df], ignore_index=True)

        drug_name_id_pairs = {}
        for idx, row in self.drugs_df.iterrows():
            drug_name_id_pairs[row['name']] = row['id']

        # id1,id2

        def lambda_fnc1(column):
            return drug_name_id_pairs[column]
        # def lambda_fnc2(row):
        #     x  = self.drugs_df[self.drugs_df['name'] == row['name2']]
        #     return x['id']

        self.ddis_df['id1'] = self.ddis_df['name1'].apply(
            lambda_fnc1)  # , axis=1
        self.ddis_df['id2'] = self.ddis_df['name2'].apply(
            lambda_fnc1)  # , axis=1
        self.drugs_df.to_sql('drug', conn, if_exists='replace', index=False)
        self.ddis_df.to_sql('event', conn, if_exists='replace', index=False)
        ZipHelper().zip_single_file(
            file_path=db_path, output_path=HERE, name='mdf-sa-ddi')


def create_connection(db_file=r"mdf-sa-ddi.db"):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_all_drugs(conn):
    cur = conn.cursor()
    cur.execute(
        '''select "index", id, name, target, enzyme, smile from drug''')
    rows = cur.fetchall()
    return rows


def select_all_drugs_as_dataframe(conn):
    headers = ['index', 'id', 'name', 'target', 'enzyme', 'smile']
    rows = select_all_drugs(conn)
    df = pd.DataFrame(columns=headers, data=rows)
    df['enzyme'] = df['enzyme'].apply(lambda x: x.split('|'))
    df['target'] = df['target'].apply(lambda x: x.split('|'))
    df['smile'] = df['smile'].apply(lambda x: x.split('|'))
    return df


def select_all_events(conn):
    """
    Query all rows in the event table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute('''
                select event."index", id1, name1, id2, name2, mechanism, action, event_category from event
                ''')

    rows = cur.fetchall()
    return rows


def select_all_events_as_dataframe(conn):
    headers = ["index", "id1", "name1", "id2",
               "name2", "mechanism", "action", "event_category"]
    rows = select_all_events(conn)
    return pd.DataFrame(columns=headers, data=rows)
