from typing import Dict, List, Tuple

from ddi_fw.ml.evaluation_helper import Metrics

class Result:
    def __init__(self) -> None:
        self.log_dict = {}
        self.metric_dict = {}

    def add_log(self, key, logs):
        self.log_dict[key] = logs

    def add_metric(self, key, metrics):
        self.metric_dict[key] = metrics


class ModelWrapper:
    def __init__(self, date, descriptor, model_func, batch_size=128, epochs=100):
        self.date = date
        self.descriptor = descriptor
        self.model_func = model_func
        self.batch_size = batch_size
        self.epochs = epochs

    def set_data(self, train_idx_arr, val_idx_arr, train_data, train_label, test_data, test_label):
        self.train_idx_arr = train_idx_arr
        self.val_idx_arr = val_idx_arr
        self.train_data = train_data
        self.train_label = train_label
        self.test_data = test_data
        self.test_label = test_label
# https://github.com/mlflow/mlflow/blob/master/examples/tensorflow/train.py

    def predict(self) -> Tuple[Dict[str, float], Metrics, List[float]]:
        pass