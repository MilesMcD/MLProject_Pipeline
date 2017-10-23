import click
#same directory import
from random_forest import RandomForestModel
from k_means    import  KMeansCluster
import sys

sys.path.append('..')
from src.data.preprocess import read_processed_data
from src.visualizations.kMeans_explore import kMeansFigures
#This function will test a Kmeans algorithm for 2-8 clusters at the moment. It saves their
#predictions and models for use in creating figures to evaluate the efficacy of this cluster count.

@click.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('output_file', type=click.Path(writable=True, dir_okay=False))
@click.option('--alg', default="rf")
#Use --alg "rf" for random forest or "km" for k-means
def main(input_file, output_file, alg):
    print('Training a model')
    if alg == "rf":
        dframe = read_processed_data(input_file)
        model = RandomForestModel()
        model.train(dframe)
        model.save(output_file)
    #reasoning behind this: https://stats.stackexchange.com/questions/9850/how-to-plot-data-output-of-clustering
    if alg == "km":
        dframe = read_processed_data(input_file)
        # Currently set to ignore categorical data in row 1
        featureOnly = dframe.loc[:, "x1":]
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
        #models[2].save(output_file)
        #create models
        kMeansFigures(predictions, models, featureOnly)

if __name__ == '__main__':
    main()
