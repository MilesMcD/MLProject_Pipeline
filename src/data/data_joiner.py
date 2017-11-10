import click
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from preprocess import preprocess_data_reg

"""
This script is used to join specific parts of two datasets for ease of access.


This data is not interpolated. That is done using the preprocess.py script interpolate functionality.
It takes 3 positional arguments: 
    The first input file (This is expected to be the larger of the 2. input 2 is "added" to it.)
    The second input file
    The output file
These arguments are relative paths. (ie: use "data/processed/xxx.pickle" to place it there.
If any inputs come from an excel spreadsheet, use the respective --fromexcel options. Their use is explained below.
"""

#Takes stuff from excel
def from_excel(dframe, sheet_num):
    return pd.read_excel(dframe, sheet_num)

#Takes stuff from .pickle files.
def read_processed_data(fname='data/processed/processed.pickle'):
    dframe = pd.read_pickle(fname)
    return dframe

"""
This function allows us to use generic labels to merge dataframes, then restore the original names to each column.
"""
def return_labels(generic, labels1, labels2):
    col_pos = ''.join(filter(lambda x: x.isdigit(), generic)) #This filters the "x"; "_x" and "_y" from the string
    if "_y" in generic:
        descriptive_label = labels2[col_pos]
    else:
        descriptive_label = labels1[col_pos]
    return descriptive_label


@click.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('input_file2', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('output_file', type=click.Path(writable=True, dir_okay=False))
@click.option('--excel', type=click.Path(writable=True, dir_okay=False))
@click.option('--fromexcel', default=-1) #variable represents sheet number. Zero base
@click.option('--fromexcel2', default=-1) #variable represents sheet number. Zero base
def main(input_file, input_file2, output_file, excel, fromexcel, fromexcel2):
    if fromexcel > -1:
        dframe = from_excel(input_file, fromexcel)
    else:
        print(input_file)
        dframe = read_processed_data(input_file)
    if fromexcel2 > -1:
        dframe2 = from_excel(input_file2, fromexcel)
    else:

        dframe2 = read_processed_data(input_file2)

    dframe, labels1 = preprocess_data_reg(dframe)

    dframe2, labels2 = preprocess_data_reg(dframe2)

    conjoined = pd.merge(left=dframe, right=dframe2.loc[dframe2['x1'] > 2004], how='left', on=['x0', 'x1'])

    conjoined.columns = [return_labels(x, labels1, labels2) for x in conjoined.columns]
    conjoined_final = conjoined


    """ THIS CODE CAN BE USED TO SPECIFY COLUMNS TO ENSURE HAVE VALUES. IT WILL DROP INDICES MISSING VALUES IN AN ENUMERATED COLUMN.
    conjoined = pd.merge(left=dframe, right=dframe2.loc[dframe2['year'] > 2004], how='left', on=['country', 'year'])
    #drop any rows without one of the 3 columns
    #conjoined = conjoined.dropna(subset=['Social support', 'GINI index (World Bank estimate)', 'Total Taxes'])
    #conjoined_final = conjoined[['country', 'year', 'Social support', 'GINI index (World Bank estimate)', 'Total Taxes']]
    """
    conjoined_final.to_pickle(output_file)

    if excel is not None:
        conjoined_final.to_excel(excel)
if __name__ == '__main__':
    main()
