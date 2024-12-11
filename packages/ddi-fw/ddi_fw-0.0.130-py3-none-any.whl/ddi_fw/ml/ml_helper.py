from typing import Dict, List, Tuple
from matplotlib import pyplot as plt
from ddi_fw.ml.model_wrapper import Result
from ddi_fw.ml.pytorch_wrapper import PTModelWrapper
from ddi_fw.ml.tensorflow_wrapper import TFModelWrapper
import tensorflow as tf
from tensorflow import keras
from keras.models import Model, Sequential
from keras.layers import Dense, Dropout, Input, Activation, BatchNormalization
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold
import numpy as np

import mlflow
from mlflow.utils.autologging_utils import batch_metrics_logger
import time

from mlflow.models import infer_signature
from ddi_fw.ml.evaluation_helper import Metrics, evaluate

# import tf2onnx
# import onnx

import itertools
import ddi_fw.utils as utils

# tf.random.set_seed(1)
# np.random.seed(2)
# np.set_printoptions(precision=4)

class MultiModalRunner:
    # todo model related parameters to config
    def __init__(self, library ,model_func, batch_size=128, epochs=100):
        self.library = library
        self.model_func = model_func
        self.batch_size = batch_size
        self.epochs = epochs
        self.result = Result()

    def set_data(self, items, train_idx_arr, val_idx_arr, y_test_label):
        self.items = items
        self.train_idx_arr = train_idx_arr
        self.val_idx_arr = val_idx_arr
        self.y_test_label = y_test_label

    def __create_multi_modal(self,library):
        if library == 'tensorflow':
            return TFModelWrapper
        elif library == 'pytorch':
            return PTModelWrapper
        else:
            raise ValueError("Unsupported library type. Choose 'tensorflow' or 'pytorch'.")

    def predict(self, combinations: list = [], generate_combinations=False):
        self.prefix = utils.utc_time_as_string()
        self.date = utils.utc_time_as_string_simple_format()
        sum = np.zeros(
            (self.y_test_label.shape[0], self.y_test_label.shape[1]))
        single_results = dict()

        if generate_combinations:
            l = [item[0] for item in self.items]
            combinations = []
            for i in range(2, len(l) + 1):
                combinations.extend(list(itertools.combinations(l, i)))  # all

        with mlflow.start_run(run_name=self.prefix, description="***") as run:
            self.level_0_run_id = run.info.run_id
            for item in self.items:
                print(item[0])
                T = self.__create_multi_modal(self.library)
                single_modal=T(self.date, item[0], self.model_func, self.batch_size, self.epochs)
                single_modal.set_data(
                    self.train_idx_arr, self.val_idx_arr, item[1], item[2], item[3], item[4])
                logs, metrics, prediction = single_modal.predict()
                # self.result.add_log(item[0], logs)
                #Check
                self.result.add_metric(item[0], metrics)
                single_results[item[0]] = prediction
                # sum = sum + prediction

            if combinations:
                self.evaluate_combinations(single_results, combinations)
        # TODO: sum'a gerek yok
        return self.result

    def evaluate_combinations(self, single_results, combinations):
        for combination in combinations:
            combination_descriptor = '-'.join(combination)
            with mlflow.start_run(run_name=combination_descriptor, description="***", nested=True) as combination_run:
                prediction = np.zeros(
                    (self.y_test_label.shape[0], self.y_test_label.shape[1]))
                for item in combination:
                    prediction = prediction + single_results[item]
                logs, metrics = evaluate(
                    actual=self.y_test_label, pred=prediction, info=combination_descriptor)
                mlflow.log_metrics(logs)
                metrics.format_float()
                # TODO path bulunamadı hatası aldık
                print(
                    f'combination_artifact_uri:{combination_run.info.artifact_uri}')
                utils.compress_and_save_data(
                    metrics.__dict__, combination_run.info.artifact_uri, f'{self.date}_metrics.gzip')
                # self.result.add_log(combination_descriptor,logs)
                # self.result.add_metric(combination_descriptor,metrics)
