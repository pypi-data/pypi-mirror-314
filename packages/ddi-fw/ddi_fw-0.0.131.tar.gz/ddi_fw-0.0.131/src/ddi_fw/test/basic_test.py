import json


class Metrics():
    def __init__(self, precision, recall, roc_aupr, roc_auc):
        self.precision = precision
        self.recall = recall
        self.roc_aupr = roc_aupr
        self.roc_auc = roc_auc


m = Metrics( 0.96, 0.96, {"micro": 0.99, "macro": 0.88}, {"micro": 0.99, "macro": 0.88})

as_json = json.dumps(m.__dict__)
print(as_json)
