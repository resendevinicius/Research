from skmultilearn.dataset import load_dataset_dump
from skmultilearn.problem_transform import BinaryRelevance
from skmultilearn.problem_transform import ClassifierChain
from sklearn import tree
from skmultilearn.adapt import MLkNN
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import KFold
from sklearn import svm
import ComplexMul as cm
import numpy as np
import sklearn.metrics as metrics
import operator

dataset = 'birds'

X_train, y_train, features_train, labels_train = load_dataset_dump('scikit_ml_learn_data/' + dataset + '-train.scikitml.bz2')
X_test, y_test, features_test, labels_test = load_dataset_dump('scikit_ml_learn_data/' + dataset + '-test.scikitml.bz2')


X = np.concatenate((X_train.toarray(), X_test.toarray()))
y = np.concatenate((y_train.toarray(), y_test.toarray()))

print(dataset)
parameters = {'k' : [5, 7, 10, 13], 'lambd' : [0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], 'threshold': [0.4, 0.5, 0.6, 0.7, 0.8, 0.9], 'classifier': [BinaryRelevance(GaussianNB()), BinaryRelevance(tree.DecisionTreeClassifier())]}
score = 'accuracy'
ks = parameters['k']
lambds = parameters['lambd']
thresholds = parameters['threshold']
classifiers = parameters['classifier']
number_splits = 5
kf = KFold(n_splits = number_splits)

scores = {}

for k in ks:
  for lambd in lambds:
    for threshold in thresholds:
      for classifier in classifiers:
        parameters_ = 'k: ' + str(k) + ' Lambda: ' + str(lambd) + ' Threshold: ' + str(threshold) + ' Classifier: ' + type(classifier).__name__ + '(' + str(classifier.classifier).split('(')[0] + ')'
        scores.update({parameters_: 0})

for train_index, test_index in kf.split(X):
  for k in ks:
    for lambd in lambds:
      for threshold in thresholds:
        for classifier in classifiers:
          model = cm.ComplexMul(k = k, classifier = classifier, lambd = lambd, threshold = threshold)
          model.fit(X[train_index], y[train_index])
          parameters_ = 'k: ' + str(k) + ' Lambda: ' + str(lambd) + ' Threshold: ' + str(threshold) + ' Classifier: ' + type(classifier).__name__ + '(' + str(classifier.classifier).split('(')[0] + ')'
          value = (metrics.accuracy_score(model.predict(X[test_index]).flatten(), y[test_index].flatten()))
          scores[parameters_] += value
      
ans = max(scores.items(), key = operator.itemgetter(1))

for key, val in scores.items():
  print(key + '\n' + 'Avg Score: ' + str(val / number_splits))

print('-----------------------------------------------------------')
print('\nBest Avg Score: ' + str(ans[1] / number_splits) + '\n' + str(ans[0]))

