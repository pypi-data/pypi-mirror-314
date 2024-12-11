from ddi_fw.ml.model_wrapper import ModelWrapper
import tensorflow as tf
from tensorflow import keras
from keras.callbacks import EarlyStopping,ModelCheckpoint
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold
import numpy as np

import mlflow
from mlflow.utils.autologging_utils import batch_metrics_logger

from mlflow.models import infer_signature
from ddi_fw.ml.evaluation_helper import Metrics, evaluate

# import tf2onnx
# import onnx

import ddi_fw.utils as utils


class TFModelWrapper(ModelWrapper):
    # https://github.com/mlflow/mlflow/blob/master/examples/tensorflow/train.py
    def predict(self):
        print(self.train_data.shape)

        # Failed to convert a NumPy array to a Tensor
        with mlflow.start_run(run_name=self.descriptor, description="***", nested=True) as run:
            models = dict()
            histories = dict()
            models_val_acc = dict()
            # with batch_metrics_logger(run_id) as metrics_logger:
            for i, (train_idx, val_idx) in enumerate(zip(self.train_idx_arr, self.val_idx_arr)):
                print(f"Validation {i}")

                with mlflow.start_run(run_name=f'Validation {i}', description='CV models', nested=True) as cv_fit:
                    model = self.model_func(self.train_data.shape[1])
                    models[f'validation_{i}'] = model
                    X_train_cv = self.train_data[train_idx]
                    y_train_cv = self.train_label[train_idx]
                    X_valid_cv = self.train_data[val_idx]
                    y_valid_cv = self.train_label[val_idx]

                    checkpoint = ModelCheckpoint(
                        filepath=f'{self.descriptor}_validation_{i}.weights.h5',
                        monitor='val_loss',
                        save_best_only=True,
                        save_weights_only=True,
                        verbose=1,
                        mode='min'
                    )

                    early_stopping = EarlyStopping(
                        monitor='val_loss', patience=10, verbose=0, mode='auto')
                    custom_callback = CustomCallback()
                    history = model.fit(X_train_cv, y_train_cv,
                                        batch_size=self.batch_size,
                                        epochs=self.epochs,
                                        validation_data=(
                                            X_valid_cv, y_valid_cv),
                                        callbacks=[early_stopping, checkpoint, custom_callback])
                    # histories[f'validation_{i}'] = history
                    # models_val_acc[f'validation_{i}'] = history.history['val_accuracy'][-1]
                    models_val_acc[f'{self.descriptor}_validation_{i}'] = checkpoint.best
                    models[f'{self.descriptor}_validation_{i}'] = checkpoint.model
                    import os
                    if os.path.exists(f'{self.descriptor}_validation_{i}.weights.h5'):
                        os.remove(f'{self.descriptor}_validation_{i}.weights.h5')
                    # Saving each CV model

            best_model_key = max(models_val_acc, key=models_val_acc.get)
            best_model = models[best_model_key]
            # mlflow.tensorflow.log_model(best_model, "model")
            # best_model.evaluate(self.test_data, self.test_label,
            #                     callbacks=[custom_callback])
            pred = best_model.predict(self.test_data)

            logs, metrics = evaluate(
                actual=self.test_label, pred=pred, info=self.descriptor)
            metrics.format_float()
            mlflow.log_metrics(logs)
            mlflow.log_param('best_cv', best_model_key)
            # signature = infer_signature(
            #     self.train_data,
            #     # generate_signature_output(model,X_valid_cv)
            #     # params=params,
            # )
            
            # mlflow.keras.save_model(
            #     best_model,
            #     path=run.info.artifact_uri + '/model',
            #     signature=signature,
            # )
            print(run.info.artifact_uri)
            # todo tf2onnx not compatible with keras > 2.15
            # onnx_model, _ = tf2onnx.convert.from_keras(
            #     best_model, input_signature=None, opset=13)
            # onnx.save(onnx_model, run.info.artifact_uri +
            #           '/model/model.onnx')
            utils.compress_and_save_data(
                metrics.__dict__, run.info.artifact_uri, f'{self.date}_metrics.gzip')

        return logs, metrics, pred


class CustomCallback(keras.callbacks.Callback):
    def on_train_begin(self, logs=None):
        keys = list(logs.keys())
        mlflow.log_param("train_begin_keys", keys)
        config = self.model.optimizer.get_config()
        for attribute in config:
            mlflow.log_param("opt_" + attribute, config[attribute])

        sum_list = []
        self.model.summary(print_fn=sum_list.append)
        summary = "\n".join(sum_list)
        mlflow.log_text(summary, artifact_file="model_summary.txt")

    def on_train_end(self, logs=None):
        print(logs)
        mlflow.log_metrics(logs)

    def on_epoch_begin(self, epoch, logs=None):
        keys = list(logs.keys())

    def on_epoch_end(self, epoch, logs=None):
        keys = list(logs.keys())

    def on_test_begin(self, logs=None):
        keys = list(logs.keys())

    def on_test_end(self, logs=None):
        mlflow.log_metrics(logs)
        print(logs)

    def on_predict_begin(self, logs=None):
        keys = list(logs.keys())

    def on_predict_end(self, logs=None):
        keys = list(logs.keys())
        mlflow.log_metrics(logs)

    def on_train_batch_begin(self, batch, logs=None):
        keys = list(logs.keys())

    def on_train_batch_end(self, batch, logs=None):
        keys = list(logs.keys())

    def on_test_batch_begin(self, batch, logs=None):
        keys = list(logs.keys())

    def on_test_batch_end(self, batch, logs=None):
        keys = list(logs.keys())

    def on_predict_batch_begin(self, batch, logs=None):
        keys = list(logs.keys())

    def on_predict_batch_end(self, batch, logs=None):
        keys = list(logs.keys())
