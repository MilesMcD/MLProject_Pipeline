import pickle
import sys
from sklearn.cluster import KMeans

sys.path.append('..')

from src.data import get_features

#nice
class KMeansCluster(object):
    def __init__(self, cluster):
        self.reg = KMeans(n_clusters=cluster, random_state=69)
        self.name = 'KMeansCluster'

    def get_params(self):
        return self.reg.get_params()

    def train(self, dframe):
        prediction = self.reg.fit_predict(dframe)
        return prediction

    def score(self, dframe):
      return self.reg.score(dframe)

    def centroids(self):
        return self.reg.cluster_centers_
#save models after prediction: write binary into an open file.
    def save(self, fname):
        with open(fname, 'wb') as openFile:
            pickle.dump(self.reg, openFile, pickle.HIGHEST_PROTOCOL)
 #load self from a file.
    def load(self, fname):
        with open(fname, 'rb') as inFile:
            self.reg = pickle.load(inFile)