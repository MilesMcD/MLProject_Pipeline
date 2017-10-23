import click
import numpy as np
import pandas as pd
#USE --EXCEL AFTER CALL TO GET CSV IN THAT FORMAT. STANDARD IN MAKEFILE.

#return features from feature 1 to the last feature before the label. (Classifier)
def get_features(dframe):
    return dframe.loc[:, 'x0':"x" + str(len(dframe)-1)]

#return labels
def get_label(dframe):
    return dframe['y']

#read in raw data
def read_raw_data(fname='src/data/raw/iris.csv'):
    dframe = pd.read_csv(fname, header=None)
    return dframe

#rename labels (classification)
def preprocess_data(dframe):
    dframe = dframe.copy()  #create new frame to ensure safety of operation.
    genericName = []
    for column in np.arange(len(dframe.columns)-1):
        genericName.append("x" + str(column))
    genericName.append("y")
    print(genericName)
    dframe.columns = genericName
    return dframe

def preprocess_data_reg(dframe):
    dframe = dframe.copy()  #create new frame to ensure safety of operation.
    genericName = []
    for column in np.arange(len(dframe.columns)):
        genericName.append("x" + str(column))
    dframe.columns = genericName
    print(genericName)
    return dframe

#read a processed frame.
#Standard output:
#'data/processed/processed.pickle'
def read_processed_data(fname='data/processed/processed.pickle'):
    dframe = pd.read_pickle(fname)
    return dframe

#main method: if this file is called alone, this is will be called. processes data.
@click.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('output_file', type=click.Path(writable=True, dir_okay=False))
@click.option('--excel', type=click.Path(writable=True, dir_okay=False))
@click.option('--cr')
#classification(cls) vs Regression (reg)
def main(input_file, output_file, excel, cr):
    print('Preprocessing data')

    dframe = read_raw_data(input_file)
    if cr == "cls":
        dframe = preprocess_data(dframe)
    if cr == "reg":
        dframe = preprocess_data_reg(dframe)
    dframe.to_pickle(output_file)
    if excel is not None:
        dframe.to_excel(excel)


if __name__ == '__main__':
    main()