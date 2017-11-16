import click
import numpy as np
import pandas as pd
from scipy.stats import zscore
from sklearn import preprocessing
import matplotlib.pyplot as plt
#USE --EXCEL AFTER CALL TO GET CSV IN THAT FORMAT. STANDARD IN MAKEFILE.


"""DOCUMENTATION
Preprocess.py is the workhorse of the pipeline. It will perform most of the processing on individual files.
As a result, it has many optional arguments that may be invoked to perform different operations. 
Each is represented by a "click.option" function decorator. Short descriptions are attached to each option.

"""


"""
Takes a sheet from an excel.
Specify a sheet number using a based 0 integer in the --fromexcel option.
"""
def from_excel(input_file, sheet_num):
        return pd.read_excel(input_file, sheet_num)

#return features from feature 1 to the last feature before the label. (Classifier)
def get_features(dframe):
    return dframe.loc[:, 'x0':"x" + str(len(dframe)-1)]

"""
Useful method for classification. Does what it says on the tin.
"""
def get_label(dframe):
    return dframe['y']

"""
Read in raw data from a csv.
"""
def read_raw_data(csvheader, fname='src/data/raw/iris.csv', ):
    if csvheader > -1:
        dframe = pd.read_csv(fname, header=csvheader)
    else:
        dframe = pd.read_csv(fname, header=None)
    return dframe

"""
Gets rid of those annoying first-line "headers" that excel users sometimes put in.
TODO:
    Just make these into headers.
"""
def removeInLineHeaders(dframe):
    df = dframe
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    return df

"""
Renames column labels to be all "Xi"s + a y column at the end for labeling.
"""
def preprocess_data(dframe):
    dframe = dframe.copy()  #create new frame to ensure safety of operation.
    genericName = []
    for column in np.arange(len(dframe.columns)-1):
        genericName.append("x" + str(column))
    genericName.append("y")
    print(genericName)
    dframe.columns = genericName
    return dframe
#preprocess unlabeled data
def preprocess_data_reg(dframe):
    dframe = dframe.copy()  #create new frame to ensure safety of operation.
    genericName = []
    labelNames = dframe.columns
    for column in np.arange(len(dframe.columns)):
        genericName.append("x" + str(column))
    dframe.columns = genericName
    return dframe, labelNames

"""
Processes a dataframe with 2 proposed manners of indexing (for instance, country and year)
This function is given 2 numbers from the --multi option. The option asks for a string formatted "x, y" for columns 1 & 2.
It will reindex the list based on these columns.
Currently, this function pulls from columns 1 & 2, which is kind of inconvenient except for the main data set of the project (happiness report).

"""
def preprocess_multi_layered_data(dframe, colPos):
    multif = dframe.set_index([dframe.columns[colPos[0]], dframe.columns[colPos[1]]])
    # First we will create a new index from the unique values in the "country" index and the range of years we want.
    # Then we simply reindex it into the data set.
    min_year = multif.index.get_level_values(1).min()
    max_year = multif.index.get_level_values(1).max()
    full_index = pd.MultiIndex.from_product(
        [multif.index.get_level_values(0).unique(), np.arange(min_year, max_year + 1)],
        names=[dframe.columns[colPos[0]], dframe.columns[colPos[1]]])
    multif = multif.reindex(full_index)
    # This will collapse our multi-index dataframe to a single index.
    dframe = multif.reset_index(level=[0, 1])
    return dframe
"""
read a processed frame from .pickle format.
Given output:
'data/processed/processed.pickle'
"""
def read_processed_data(fname='data/processed/processed.pickle'):
    dframe = pd.read_pickle(fname)
    return dframe

"""
Takes a non-index dataframe with index to slice by in column 0.
 Linearly Interpolates all non-indexed columns from first recording in an index. (All besides column 0)
"""
def interpolate_dataframe(dframe):
    # index by country so we can target slices.
    index_countries = dframe.set_index([dframe.columns[0]], drop=False)
    ##Divide the dataset into slices for interpolation.
    for i in range(len(index_countries.index.unique())):
        index_countries.loc[index_countries.index.unique()[i], :] = index_countries.loc[
                                                                    index_countries.index.unique()[i], :] \
            .interpolate(fill_direction="both")
    # Fix index
    dframe = index_countries.reset_index(drop=True)
    return dframe

"""
Drops entries that are missing a value.
"""
def dropNA(dframe):
    dframe = dframe.replace(0, float('nan'))
    dframe = dframe.dropna()
    return dframe

#main method: if this file is called alone, this is will be called. processes data.
@click.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('output_file', type=click.Path(writable=True, dir_okay=False))

@click.option('--excel', type=click.Path(writable=True, dir_okay=False))#Create excel spreadsheet clone of output.

@click.option('--csvheader', default=-1) #Fixes CSV headers. Don't use fixheader on CSVs. Assumes no header. Use 0 otherwise.

@click.option('--cr') #if headers need to be changed. Refer to preprocess_data & preprocess_data_reg functions.

@click.option('--fixheader', default=False)#Used on excel spreadsheets to fix headers.

@click.option('--fromexcel', default=-1) #variable represents sheet number. Zero base

@click.option('--multi', default="") #FORMAT IS (column_position_1, column_position_2) IN INTEGER FORM.

@click.option('--intrpl', default=False)#Interpolates if true

@click.option('--dropna', default=False)#drops ALL entries with a null value if true. DANGEROUS.

@click.option('--preprocessed', default=False)#Set True if dataset is coming in from a pickle file.

@click.option('--normalize', default=False)#Set to True to zscore all numeric columns.

@click.option('--getaverages', default=-1) #group by a column. Zero base. Returns mean values for each country.

def main(input_file, output_file, excel, cr, fixheader, fromexcel, multi, intrpl, dropna, preprocessed, normalize, getaverages, csvheader):
    print('Preprocessing data')
    if fromexcel > -1:
        dframe = from_excel(input_file, fromexcel)
    elif preprocessed:
        dframe = read_processed_data(input_file)
    else:
        dframe = read_raw_data(csvheader, input_file)
    #Classifiers
    if cr == "cls":
        dframe = preprocess_data(dframe)
    #Regression
    if cr == "reg":
        dframe = preprocess_data_reg(dframe)
    # Fixes in-line headers
    if fixheader:
        dframe = removeInLineHeaders(dframe)

    if len(multi) > 1: #Please check Documentation
        #List Comprehension to convert to column positions
        colPosStr = [x.strip() for x in multi.split(',')]
        colPosInt = [int(x) for x in colPosStr]
        dframe = preprocess_multi_layered_data(dframe, colPosInt)

    if intrpl: #Please check Documentation
        dframe = interpolate_dataframe(dframe)

    if dropna:
        dframe = dropNA(dframe)

    if normalize:
        # Scale data.
        numeric_cols = dframe.select_dtypes(include=[np.number]).columns
        dframe = dframe[numeric_cols].apply(zscore)
        """
        for i in range(normalize, len(dframe.columns)):
            curr_col = dframe.columns[i]
            dframe[curr_col] = dframe[curr_col].apply(lambda x: 2 * ((x - dframe[curr_col].min()) /
                                                                          (dframe[curr_col].max() - dframe[
                                                                       curr_col].min())) - 1)
        """
    if getaverages > -1:
        #dframe = dframe.drop(["year"], axis=1) USE THIS IF IT WOULD BE CONVENIENT TO REMOVE A COLUMN.
        grouped = dframe.groupby(dframe.columns[getaverages])
        dframe = grouped.mean()

    dframe.to_pickle(output_file)
    #adds excel sheet output.
    if excel is not None:
        dframe.to_excel(excel)
if __name__ == '__main__':
    main()
