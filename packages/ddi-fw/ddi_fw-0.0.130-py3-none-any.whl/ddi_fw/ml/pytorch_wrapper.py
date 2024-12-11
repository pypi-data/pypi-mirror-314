import mlflow
import torch
from ddi_fw.ml.evaluation_helper import evaluate
from ddi_fw.ml.model_wrapper import ModelWrapper


class PTModelWrapper(ModelWrapper):
    def __init__(self, date, descriptor, model_func, batch_size=128, epochs=100, **kwargs):
        super().__init__(date, descriptor, model_func, batch_size, epochs)
        self.optimizer = kwargs['optimizer']
        self.criterion = kwargs['criterion']

    def _create_dataloader(self, data, labels):
        dataset = torch.utils.data.TensorDataset(data, labels)
        return torch.utils.data.DataLoader(dataset, batch_size=self.batch_size, shuffle=True)

    def predict(self):
        print(self.train_data.shape)

        with mlflow.start_run(run_name=self.descriptor, description="***", nested=True) as run:
            models = {}
            # models_val_acc = {}

            for i, (train_idx, val_idx) in enumerate(zip(self.train_idx_arr, self.val_idx_arr)):
                print(f"Validation {i}")

                with mlflow.start_run(run_name=f'Validation {i}', description='CV models', nested=True) as cv_fit:
                    model = self.model_func(self.train_data.shape[1])
                    models[f'validation_{i}'] = model

                    # Create DataLoaders
                    X_train_cv = torch.tensor(self.train_data[train_idx], dtype=torch.float16)
                    y_train_cv = torch.tensor(self.train_label[train_idx], dtype=torch.float16)
                    X_valid_cv = torch.tensor(self.train_data[val_idx], dtype=torch.float16)
                    y_valid_cv = torch.tensor(self.train_label[val_idx], dtype=torch.float16)

                    train_loader = self._create_dataloader(X_train_cv, y_train_cv)
                    valid_loader = self._create_dataloader(X_valid_cv, y_valid_cv)

                    optimizer = self.optimizer
                    criterion = self.criterion
                    best_val_loss = float('inf')

                    for epoch in range(self.epochs):
                        model.train()
                        for batch_X, batch_y in train_loader:
                            optimizer.zero_grad()
                            output = model(batch_X)
                            loss = criterion(output, batch_y)
                            loss.backward()
                            optimizer.step()

                        model.eval()
                        with torch.no_grad():
                            val_loss = self._validate(model, valid_loader)

                        # Callbacks after each epoch
                        for callback in self.callbacks:
                            callback.on_epoch_end(epoch, logs={'loss': loss.item(), 'val_loss': val_loss.item()})

                        if val_loss < best_val_loss:
                            best_val_loss = val_loss
                            best_model = model

                    # Evaluate on test data
                    with torch.no_grad():
                        pred = best_model(torch.tensor(self.test_data, dtype=torch.float16))
                        logs, metrics = evaluate(
                            actual=self.test_label, pred=pred.numpy(), info=self.descriptor)
                        mlflow.log_metrics(logs)

            return logs, metrics, pred.numpy()

    def _validate(self, model, valid_loader):
        total_loss = 0
        criterion = self.criterion

        for batch_X, batch_y in valid_loader:
            output = model(batch_X)
            loss = criterion(output, batch_y)
            total_loss += loss.item()

        return total_loss / len(valid_loader)