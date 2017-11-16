import click
#same directory import
from random_forest import RandomForestModel
from k_means    import  KMeansCluster
from svm_regression import svm_regressor
from sklearn.model_selection import train_test_split
import sys

sys.path.append('..')
from src.data.preprocess import read_processed_data
from src.visualizations.kMeans_explore import kMeansFigures

"""
#This function will test a Kmeans algorithm for 2-8 clusters at the moment. It creates an array of
predictions and models for use in creating figures to evaluate the efficacy of this cluster count.


UNFINISHED: Incomplete options / Incomplete helper class: k_means.py
A model with X number of clusters must manually be entered into the code at the moment if the model is to be saved.
"""


@click.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('output_file', type=click.Path(writable=True, dir_okay=False))
@click.option('--alg', default="km")
#Use --alg "rf" for random forest, "svr" for support vector regression, or "km" for k-means
def main(input_file, output_file, alg):
    print('Training a model')
    if alg == "rf":
        dframe = read_processed_data(input_file)
        featureSet, labelSet = train_test_split(dframe[:, :-1], dframe[:, -1:])
        model = RandomForestModel()
        model.train(featureSet)
        model.score(labelSet)
        model.save(output_file)
        #trained.save(output_file)
    if alg == "svr":
        #split data into training and testing sets.
        dframe = read_processed_data(input_file)
        train_set, test_set = train_test_split(dframe)
        model = svm_regressor()
        model.train(train_set)
        print(model.score(test_set))
        # trained.save(output_file)
    #reasoning behind this: https://stats.stackexchange.com/questions/9850/how-to-plot-data-output-of-clustering
    if alg == "km":
        dframe = read_processed_data(input_file)
        # Currently set to ignore categorical data in row 1
        featureOnly = dframe.loc[:, dframe.columns[0]:]
        print(featureOnly.shape)
#TOTAL CLUSTER COUNT: CHANGE AS NECESSARY
        models = []
        predictions = []

        print("scoring models by cluster count: ")
        for i in range(2, 8):
            model = KMeansCluster(i)
            #we're going to save model predictions as well as the models themselves.
            predictions.append(model.train(featureOnly))
            print(i)
            print(model.score(featureOnly))
            models.append(model)

        """
        INCOMPLETE: CHANGE CODE HERE TO SAVE OR PRINT MODELS.
        """
        ## create model file
        #models[3].save(output_file)

        ##Create list of predicted labels.
        cluster_7_labels = predictions[5]
        dframe['labels'] = cluster_7_labels

        ##This line can be set manually to send labelled datasets to an excel sheet.
        #dframe.sort(["labels"]).to_excel("data/processed/hsgt.xlsx")
        for i in range(7):
            print(dframe[dframe['labels'] == i])
        kMeansFigures(predictions, models, featureOnly)


if __name__ == '__main__':
    main()
