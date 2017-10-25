import click
import numpy as np
import pandas as pd
#USE --EXCEL AFTER CALL TO GET CSV IN THAT FORMAT. STANDARD IN MAKEFILE.

def from_excel(dframe, sheet_num):
        return pd.read_excel(dframe, sheet_num)

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

#Put in-line headers into the actual header position. Assuming they are at row 0.
def removeInLineHeaders(dframe):
    df = dframe
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    return df

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
@click.option('--fixheader', default=False)
@click.option('--fromexcel', default=-1) #variable represents sheet number. Zero base
@click.option('--multi', default=False)
#classification(cls) vs Regression (reg)
def main(input_file, output_file, excel, cr, fixheader, fromexcel, multi):
    print('Preprocessing data')
    dframe = pd.DataFrame
    if fromexcel > -1:
        dframe = from_excel(input_file, fromexcel)
    else:
        dframe = read_raw_data(input_file)
    #Classifiers
    if cr == "cls":
        dframe = preprocess_data(dframe)
    #Regression
    if cr == "reg":
        dframe = preprocess_data_reg(dframe)
    # Fixes in-line headers
    if fixheader:
        dframe = removeInLineHeaders(dframe)

    if multi: #CHANGE THIS BY DATASET
        multif = dframe.set_index([dframe.columns[1], dframe.columns[2]])
        #First we will create a new index from the unique values in the "country" index and the range of years we want.
        #Then we simply reindex it into the data set.
        min_year = multif.index.get_level_values(1).min()
        max_year = multif.index.get_level_values(1).max()
        full_index = pd.MultiIndex.from_product(
            [multif.index.get_level_values(0).unique(), np.arange(min_year, max_year+1)], names=[dframe.columns[1], dframe.columns[2]])
        multif = multif.reindex(full_index)
        #This will collapse our multi-index dataframe to a single index.
        dframe = multif.reset_index(level=[0, 1])
    dframe.to_pickle(output_file)

    #adds excel sheet output.
    if excel is not None:
        dframe.to_excel(excel)
if __name__ == '__main__':
    main()