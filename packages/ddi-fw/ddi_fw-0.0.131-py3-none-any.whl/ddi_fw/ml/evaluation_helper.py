import numpy as np
from sklearn import metrics
from sklearn.metrics import accuracy_score, precision_recall_curve
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import auc
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder

def __format__(d,floating_number_precision = 4):
    if type(d) is dict:
        d = {k: __round__(v,floating_number_precision) for k, v in d.items()}
    else:
        d = round(d,floating_number_precision)
    return d

def __round__(v,floating_number_precision = 4):
    if type(v) is list or type(v) is set:
       return [round(item,floating_number_precision) for item in v]
    else:
        return round(v,floating_number_precision)


class Metrics():
    def __init__(self, label):
        self.label = label

    def classification_report(self,classification_report):
        self.classification_report = classification_report

    def accuracy(self, accuracy):
        self.accuracy = accuracy

    def precision(self, precision):
        self.precision = precision

    def recall(self, recall):
        self.recall = recall

    def f1_score(self, f1_score):
        self.f1_score = f1_score

    def roc_auc(self, roc_auc):
        self.roc_auc = roc_auc

    def roc_aupr(self, roc_aupr):
        self.roc_aupr = roc_aupr

    def format_float(self, floating_number_precision = 4):
        self.accuracy = round(self.accuracy,floating_number_precision)
        self.precision = __format__( self.precision ,floating_number_precision)
        self.recall = __format__( self.recall ,floating_number_precision)
        self.f1_score = __format__( self.f1_score ,floating_number_precision)
        self.roc_auc = __format__( self.roc_auc ,floating_number_precision)
        self.roc_aupr = __format__( self.roc_aupr ,floating_number_precision)


# taken from https://github.com/YifanDengWHU/DDIMDL/blob/master/DDIMDL.py#L214
def roc_aupr_score(y_true, y_score, average="macro"):
    def _binary_roc_aupr_score(y_true, y_score):
        precision, recall, pr_thresholds = precision_recall_curve(
            y_true, y_score)
        # precision, recall, pr_thresholds = metrics.roc_curve(y, pred, pos_label=2)
        return auc(precision, recall)

    def _average_binary_score(binary_metric, y_true, y_score, average):  # y_true= y_one_hot
        if average == "binary":
            return binary_metric(y_true, y_score)
        if average == "micro":
            y_true = y_true.ravel()
            y_score = y_score.ravel()
        if y_true.ndim == 1:
            y_true = y_true.reshape((-1, 1))
        if y_score.ndim == 1:
            y_score = y_score.reshape((-1, 1))
        n_classes = y_score.shape[1]
        score = np.zeros((n_classes,))
        for c in range(n_classes):
            y_true_c = y_true.take([c], axis=1).ravel()
            y_score_c = y_score.take([c], axis=1).ravel()
            score[c] = binary_metric(y_true_c, y_score_c)
        return np.average(score)

    return _average_binary_score(_binary_roc_aupr_score, y_true, y_score, average)


def evaluate(actual, pred, info='', print=False):
    # Precompute y_true and y_pred
    y_true = np.argmax(actual, axis=1)
    y_pred = np.argmax(pred, axis=1)
    
    # Generate classification report
    c_report = classification_report(y_true, y_pred, output_dict=True)
    
    # Metrics initialization
    metrics = Metrics(info)
    
    n_classes = actual.shape[1]
    
    precision = {}
    recall = {}
    f_score = {}
    roc_aupr = {}
    roc_auc = {
        "weighted": 0,
        "macro": 0,
        "micro": 0
    }

    # Preallocate lists
    precision_vals = [[] for _ in range(n_classes)]
    recall_vals = [[] for _ in range(n_classes)]

    # Compute metrics for each class
    for i in range(n_classes):
        precision_vals[i], recall_vals[i], _ = precision_recall_curve(
            actual[:, i], pred[:, i])
        roc_aupr[i] = auc(recall_vals[i], precision_vals[i])

    # Calculate ROC AUC scores
    roc_auc["weighted"] = roc_auc_score(actual, pred, multi_class='ovr', average='weighted')
    roc_auc["macro"] = roc_auc_score(actual, pred, multi_class='ovr', average='macro')
    roc_auc["micro"] = roc_auc_score(actual, pred, multi_class='ovr', average='micro')

    # Micro-average Precision-Recall curve and ROC-AUPR
    precision["micro_event"], recall["micro_event"], _ = precision_recall_curve(actual.ravel(), pred.ravel())
    roc_aupr["micro"] = auc(recall["micro_event"], precision["micro_event"])

    # Convert lists to numpy arrays for better performance
    precision["micro_event"] = precision["micro_event"].tolist()
    recall["micro_event"] = recall["micro_event"].tolist()

    # Overall accuracy
    acc = accuracy_score(y_true, y_pred)

    # Aggregate precision, recall, and f_score
    for avg_type in ['weighted', 'macro', 'micro']:
        precision[avg_type] = precision_score(y_true, y_pred, average=avg_type)
        recall[avg_type] = recall_score(y_true, y_pred, average=avg_type)
        f_score[avg_type] = f1_score(y_true, y_pred, average=avg_type)

    if print:
        print(
            f'''Accuracy: {acc}
            , Precision:{precision['weighted']}
            , Recall: {recall['weighted']}
            , F1-score: {f_score['weighted']}
            ''')

    logs = {'accuracy': acc,
            'weighted_precision': precision['weighted'],
            'macro_precision': precision['macro'],
            'micro_precision': precision['micro'],
            'weighted_recall_score': recall['weighted'],
            'macro_recall_score': recall['macro'],
            'micro_recall_score': recall['micro'],
            'weighted_f1_score': f_score['weighted'],
            'macro_f1_score': f_score['macro'],
            'micro_f1_score': f_score['micro'],
            # 'weighted_roc_auc_score': weighted_roc_auc_score,
            # 'macro_roc_auc_score': macro_roc_auc_score,
            # 'micro_roc_auc_score': micro_roc_auc_score,
            # 'macro_aupr_score': macro_aupr_score,
            # 'micro_aupr_score': micro_aupr_score
            "micro_roc_aupr": roc_aupr['micro'],
            # "micro_precision_from_precision_recall_curve":precision["micro"],
            # "micro_recall_from_precision_recall_curve":recall["micro"],
            "weighted_roc_auc": roc_auc['weighted'],
            "macro_roc_auc": roc_auc['macro'],
            "micro_roc_auc": roc_auc['micro']
            }
    metrics.accuracy(acc)
    metrics.precision(precision)
    metrics.recall(recall)
    metrics.f1_score(f_score)
    metrics.roc_auc(roc_auc)
    metrics.roc_aupr(roc_aupr)
    metrics.classification_report(c_report)
    return logs, metrics


# actual and pred are one-hot encoded
def evaluate_ex(actual, pred, info = '' ,print=False):
    
    y_pred = np.argmax(pred, axis=1)
    y_true = np.argmax(actual, axis=1)
    c_report = classification_report(y_true, y_pred, output_dict = True)
    

    metrics = Metrics(info)

    precision = dict()
    recall = dict()
    f_score = dict()
    roc_aupr = dict()
    roc_auc = dict()

    # Compute Precision-Recall and ROC-AUPR for each class
    for i in range(actual.shape[1]):
        precision[i], recall[i], _ = precision_recall_curve(
            actual[:, i].ravel(), pred[:, i].ravel())
        roc_aupr[i] = auc(recall[i], precision[i])
        precision[i] = precision[i].tolist()
        recall[i] = recall[i].tolist()
        classes = [1 if i == np.argmax(y) else 0 for y in y_true]
        # roc_auc[i] = roc_auc_score(classes, pred[:,i])

    roc_auc["weighted"] = roc_auc_score(
        actual, pred, multi_class='ovr', average='weighted')
    roc_auc["macro"] = roc_auc_score(
        actual, pred, multi_class='ovr', average='macro')
    roc_auc["micro"] = roc_auc_score(
        actual, pred, multi_class='ovr', average='micro')

    # Compute micro-average Precision-Recall curve and ROC-AUPR
    precision["micro_event"], recall["micro_event"], _ = precision_recall_curve(
        actual.ravel(), pred.ravel())
    roc_aupr["micro"] = auc(recall["micro_event"], precision["micro_event"])
    precision["micro_event"] = precision["micro_event"].tolist()
    recall["micro_event"] = recall["micro_event"].tolist()
    # weighted_roc_auc_score = roc_auc_score(actual, pred, multi_class='ovr', average='weighted')
    # macro_roc_auc_score = roc_auc_score(actual, pred, multi_class='ovr', average='macro')
    # micro_roc_auc_score = roc_auc_score(actual, pred, multi_class='ovr', average='micro')

    # macro_aupr_score = roc_aupr_score(actual, pred, average='macro')
    # micro_aupr_score = roc_aupr_score(actual, pred, average='micro')

    acc = accuracy_score(y_true, y_pred)

    precision['weighted'] = precision_score(y_true, y_pred, average='weighted')
    precision['macro'] = precision_score(y_true, y_pred, average='macro')
    precision['micro'] = precision_score(y_true, y_pred, average='micro')

    recall['weighted'] = recall_score(y_true, y_pred, average='weighted')
    recall['macro'] = recall_score(y_true, y_pred, average='macro')
    recall['micro'] = recall_score(y_true, y_pred, average='micro')

    f_score['weighted'] = f1_score(y_true, y_pred, average='weighted')
    f_score['macro'] = f1_score(y_true, y_pred, average='macro')
    f_score['micro'] = f1_score(y_true, y_pred, average='micro')

    # acc = accuracy_score(y_true, y_pred)

    # weighted_precision = precision_score(y_true, y_pred, average='weighted')
    # macro_precision = precision_score(y_true, y_pred, average='macro')
    # micro_precision = precision_score(y_true, y_pred, average='micro')

    # weighted_recall_score = recall_score(y_true, y_pred, average='weighted')
    # macro_recall_score = recall_score(y_true, y_pred, average='macro')
    # micro_recall_score = recall_score(y_true, y_pred, average='micro')

    # weighted_f1_score = f1_score(y_true, y_pred, average='weighted')
    # macro_f1_score = f1_score(y_true, y_pred, average='macro')
    # micro_f1_score = f1_score(y_true, y_pred, average='micro')

    if print:
        print(
            f'''Accuracy: {acc}
            , Precision:{precision['weighted']}
            , Recall: {recall['weighted']}
            , F1-score: {f_score['weighted']}
            ''')

    logs = {'accuracy': acc,
            'weighted_precision': precision['weighted'],
            'macro_precision': precision['macro'],
            'micro_precision': precision['micro'],
            'weighted_recall_score': recall['weighted'],
            'macro_recall_score': recall['macro'],
            'micro_recall_score': recall['micro'],
            'weighted_f1_score': f_score['weighted'],
            'macro_f1_score': f_score['macro'],
            'micro_f1_score': f_score['micro'],
            # 'weighted_roc_auc_score': weighted_roc_auc_score,
            # 'macro_roc_auc_score': macro_roc_auc_score,
            # 'micro_roc_auc_score': micro_roc_auc_score,
            # 'macro_aupr_score': macro_aupr_score,
            # 'micro_aupr_score': micro_aupr_score
            "micro_roc_aupr": roc_aupr['micro'],
            # "micro_precision_from_precision_recall_curve":precision["micro"],
            # "micro_recall_from_precision_recall_curve":recall["micro"],
            "weighted_roc_auc": roc_auc['weighted'],
            "macro_roc_auc": roc_auc['macro'],
            "micro_roc_auc": roc_auc['micro']
            }
    metrics.accuracy(acc)
    metrics.precision(precision)
    metrics.recall(recall)
    metrics.f1_score(f_score)
    metrics.roc_auc(roc_auc)
    metrics.roc_aupr(roc_aupr)
    metrics.classification_report(c_report)
    return logs, metrics


# # Sample integer array
# integer_array = np.array([0, 1, 2, 1, 0])

# # Reshape the integer array to a column vector
# integer_array = integer_array.reshape(-1, 1)

# # Create OneHotEncoder object
# encoder = OneHotEncoder(sparse_output=False)

# # Fit and transform the integer array to one-hot encoded array
# y_true = encoder.fit_transform(integer_array)
# # y_true = np.array([[1, 0, 0],
# #                    [0, 1, 0],
# #                    [0, 0, 1],
# #                    [1, 0, 0],
# #                    [0, 0, 1]],
# #                    )
# y_score = np.array([[0.6, 0.2, 0.2],
#                     [0.2, 0.5, 0.3],
#                     [0.1, 0.2, 0.7],
#                     [0.1, 0.8, 0.1],
#                     [0.1, 0.6, 0.3]])

# y = np.array([-1, -1, 1, 1])
# pred = np.array([0.1, 0.4, 0.35, 0.8])
# evaluate(y_true,y_score)
# fpr, tpr, thresholds = metrics.roc_curve(y, pred)
# print(metrics.auc(fpr, tpr))
# print(roc_aupr_score(y,pred))
