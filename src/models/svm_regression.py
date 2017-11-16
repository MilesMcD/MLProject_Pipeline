import pickle
import sys
from sklearn.svm import SVR

sys.path.append('..')

from src.data import get_features
"""
Implementation of the sklearn library's SVM.SVR Support Vector Regressor as an object, so that it can be saved as a model.  

Note: All data coming into this algorithm should be normalized uniformly.

UNFINISHED: Tuning must be done in the file.
"""
#nice
class svm_regressor(object):
    def __init__(self):
        self.reg = SVR(cache_size=500)
        self.name = 'svm_regressor'

    def get_params(self):
        return self.reg.get_params()

    def train(self, dframe):
        prediction = self.reg.fit(dframe.iloc[:, :-1], dframe.iloc[:, -1])
        return prediction

    def score(self, dframe):
        return self.reg.score(dframe.iloc[:, :-1], dframe.iloc[:, -1])


#save models after prediction: write binary into an open file.
    def save(self, fname):
        with open(fname, 'wb') as openFile:
            pickle.dump(self.reg, openFile, pickle.HIGHEST_PROTOCOL)
 #load self from a file.
    def load(self, fname):
        with open(fname, 'rb') as inFile:
            self.reg = pickle.load(inFile)