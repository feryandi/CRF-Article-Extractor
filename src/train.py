from itertools import chain

import pycrfsuite
import pickle

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer

def print_classification_report(y_true, y_pred):
  """
  Classification report for a list of BIO-encoded sequences.
  It computes token-level metrics and discards "O" labels.
  
  Note that it requires scikit-learn 0.15+ (or a version from github master)
  to calculate averages properly!
  """
  lb = LabelBinarizer()
  y_true_combined = lb.fit_transform(list(chain.from_iterable(y_true)))
  y_pred_combined = lb.transform(list(chain.from_iterable(y_pred)))
      
  tagset = set(lb.classes_) - {'O'}
  tagset = sorted(tagset, key=lambda tag: tag.split('-', 1)[::-1])
  class_indices = {cls: idx for idx, cls in enumerate(lb.classes_)}
  
  print(classification_report(
      y_true_combined,
      y_pred_combined,
      labels = [class_indices[cls] for cls in tagset],
      target_names = tagset,
  ))
  
  print(confusion_matrix(y_true_combined, 
    y_pred_combined,
    labels = [class_indices[cls] for cls in tagset]
  ))

  print('\n')

def main():
  model = 'model/html-content-extractor.crfsuite'
  X = pickle.load(open('pickle/train.x.p', 'rb'))
  y = pickle.load(open('pickle/train.y.p', 'rb'))

  trainer = pycrfsuite.Trainer(verbose=False)

  for xseq, yseq in zip(X, y):
    trainer.append(xseq, yseq)

  trainer.train(model)
  tagger = pycrfsuite.Tagger()
  tagger.open(model)

  setdata = ['validation', 'test']
  for s in setdata:
    print('Clasification Report from %s Data' % s)
    X_test = pickle.load(open('pickle/%s.x.p' % s, 'rb'))
    y_test = pickle.load(open('pickle/%s.y.p' % s, 'rb'))

    y_pred = [tagger.tag(xseq) for xseq in X_test]
    print_classification_report(y_test, y_pred)

if __name__ == "__main__":
  main()
