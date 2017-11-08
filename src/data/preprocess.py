import click
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#USE --EXCEL AFTER CALL TO GET CSV IN THAT FORMAT. STANDARD IN MAKEFILE.

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
def read_raw_data(fname='src/data/raw/iris.csv'):
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
    for column in np.arange(len(dframe.columns)):
        genericName.append("x" + str(column))
    dframe.columns = genericName
    print(genericName)
    return dframe

"""
Processes a dataframe with 2 proposed manners of indexing (for instance, country and year)
Currently, this function pulls from columns 1 & 2, which is kind of inconvenient except for the main data set of the project (happiness report).

"""
def preprocess_multi_layered_data(dframe):
    multif = dframe.set_index([dframe.columns[1], dframe.columns[2]])
    # First we will create a new index from the unique values in the "country" index and the range of years we want.
    # Then we simply reindex it into the data set.
    min_year = multif.index.get_level_values(1).min()
    max_year = multif.index.get_level_values(1).max()
    full_index = pd.MultiIndex.from_product(
        [multif.index.get_level_values(0).unique(), np.arange(min_year, max_year + 1)],
        names=[dframe.columns[1], dframe.columns[2]])
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

#main method: if this file is called alone, this is will be called. processes data.
@click.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('output_file', type=click.Path(writable=True, dir_okay=False))
@click.option('--excel', type=click.Path(writable=True, dir_okay=False))
@click.option('--cr')
@click.option('--fixheader', default=False)
@click.option('--fromexcel', default=-1) #variable represents sheet number. Zero base
@click.option('--multi', default=False)
@click.option('--intrpl', default=False)
@click.option('--diff', default=False)
@click.option('--preprocessed', default=False)
#classification(cls) vs Regression (reg)
def main(input_file, output_file, excel, cr, fixheader, fromexcel, multi, intrpl, diff, preprocessed):
    print('Preprocessing data')
    if fromexcel > -1:
        dframe = from_excel(input_file, fromexcel)
    elif preprocessed:
        dframe = read_processed_data(input_file)
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

    if multi: #Please check Documentation
        dframe = preprocess_multi_layered_data(dframe)

    if intrpl: #Please check Documentation
        dframe = interpolate_dataframe(dframe)
    if diff:
        dframe = dframe.diff()
        print(dframe.iloc[0:5])

    dframe.to_pickle(output_file)
    #adds excel sheet output.
    if excel is not None:
        dframe.to_excel(excel)
if __name__ == '__main__':
    main()