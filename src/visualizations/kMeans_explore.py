import click
import sys
from sklearn.metrics import silhouette_samples, silhouette_score

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D #this is necessary.
sys.path.append('..')
from src.data import read_processed_data


"""
This script allows visualization of kmeans algorithms with 2 or 3 dimensions. 
It takes a set of predictions, a set of models, and the dataframe used.

"""


def kMeansFigures(predictions, kArray, dframe):
    #DATAFRAME INDEX COUNT
    samples = len(dframe.index)
    #NUMBER OF MODELS
    count = len(predictions)
    print(len(predictions))
    #iterate through predictions array
    iterator = 0
    #CLUSTER IS # OF CLUSTERS
    for cluster in range(2, count+2):
        # SET UP SILHOUETTE PLOT & 3D PLOT
        fig = plt.figure()
        (ax1) = fig.add_subplot(221)
        #row, column, plot number
        ax2 = fig.add_subplot(222, projection='3d')
        fig.set_size_inches(18, 7)

        #silhouette plot ranges from -1 to 1
        ax1.set_xlim([-1, 1])
        ax1.set_ylim([0, samples + (count + 1) * 10]) #creating space between subfigures
        #silhouette score tells us about cluster density. (and separation)
        silhAvg = silhouette_score(dframe, predictions[iterator])
        print(cluster, silhAvg, sep="    clusters // silhouette average   ")
        #silhouette samples will show us the quality of our clusters.
        silhValues = silhouette_samples(dframe, predictions[iterator])

        #FORMAT AND COLOR SILHOUETTE PLOT
        y_low = 10 #get some distance between new plots
        for i in range(cluster):
            #get values & size from this cluster.
            i_cluster_silhVal = silhValues[predictions[iterator] == i]
            i_cluster_silhVal.sort()
            cluster_size = i_cluster_silhVal.shape[0] #size of cluster
            y_up = y_low + cluster_size
            colorSet = cm.spectral(float(i) / cluster)
            ax1.fill_betweenx(np.arange(y_low, y_up), 0, i_cluster_silhVal, facecolors=colorSet,
                              edgecolor=colorSet, alpha=.8)
            #label plot
            ax1.text(-.05, y_low + .5 * cluster_size, str(i))
            y_low = y_up + 10 #get more space for next cluster

        ax1.set_title("Silhouette Comparison Plot")
        ax1.set_xlabel("Coefficient Values")
        ax1.set_ylabel("Cluster")
        ax1.axvline(x=silhAvg, color="orange", linestyle="--") #average value of silhouette.

        ax1.set_yticks([]) #don't need these
        xTick = []
        for i in np.arange(-1, 1.1, .1):
            xTick.append(i)
        ax1.set_xticks(xTick) #get ticks on each .1 for x axis.

        #PLOT NUMBER 2:

        #2D
        if dframe.shape[1] == 2:
            ax2.set_title("Cluster Visualization")
            ax2.set_xlabel(dframe.columns[0])
            ax2.set_ylabel(dframe.columns[1])
            colors = cm.spectral(float(i) / cluster)
            #scatter plot: x, y, dot-markker, point size, opacity, spectral color, dot edgecolors.
            ax2.scatter(dframe.iloc[:, 0], dframe.iloc[:, 1], marker='.', s=30, alpha = .69, c=colors, edgecolor='k')
            #show centroids:
            centroids = kArray[cluster].centroids()
            #x, y, x-marker, opaque, white.
            ax2.scatter(centroids[:,0], centroids[:, 1], marker='x', s=150, c="white", alpha=1, edgecolor='k')

        #3D
        if dframe.shape[1] == 3:

            #BEGIN PROJECT DATA LABELS
            ax2.set_title("Cluster Visualization")
            ax2.set_xlabel(dframe.columns[0])
            ax2.set_ylabel(dframe.columns[1])
            ax2.set_zlabel(dframe.columns[2])
            #END PROJECT DATA LABELS
            #dframe[:, 0, 0], dframe[0, :, 0], dframe[0, 0, :]
            colors3D = cm.spectral(predictions[iterator].astype(float) / cluster)
            ax2.scatter(dframe.iloc[:, 0], dframe.iloc[:, 1], dframe.iloc[:, 2], s=30, c=colors3D)
            centroids = kArray[iterator].centroids()
            ax2.scatter(centroids[:, 0], centroids[:, 1], centroids[:, 2], s=200, c='grey', marker='x', alpha=1)

        iterator += 1
        plt.show()
