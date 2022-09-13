import numpy as np
import sklearn

from sklearn.metrics import precision_recall_fscore_support

y_true = np.array(['cat', 'dog', 'pig', 'cat', 'dog', 'pig'])
y_pred = np.array(['cat', 'pig', 'dog', 'cat', 'cat', 'dog'])

precision_recall_fscore_support(y_true, y_pred, average='macro')
precision_recall_fscore_support(y_true, y_pred, average='micro')
precision_recall_fscore_support(y_true, y_pred, average='weighted')
