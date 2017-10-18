import pickle
import sys

from sklearn.ensemble import RandomForestClassifier

sys.path.append('..')

from src.data import get_features, get_label


class RandomForestModel(object):
    def __init__(self):
        self.clf = RandomForestClassifier(n_estimators=75, max_depth=650)
        self.name = 'RandomForest'

    def get_params(self):
        return self.clf.get_params()

    def train(self, dframe):
        x = get_features(dframe)
        y = get_label(dframe)
        self.clf.fit(x, y)

    def predict(self, x):
        y_pred = self.clf.predict(x)

        return y_pred
#save models after prediction: write binary into an open file.
    def save(self, fname):
        with open(fname, 'wb') as openFile:
            pickle.dump(self.clf, openFile, pickle.HIGHEST_PROTOCOL)
 #load self from a file.
    def load(self, fname):
        with open(fname, 'rb') as inFile:
            self.clf = pickle.load(inFile)