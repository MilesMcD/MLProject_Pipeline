import click
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
This script is being used to join specific parts of two datasets for ease of access.
Currently, it joins together social inclusion, gini index, & tax rate as % of income.
This data is not interpolated. That is done using the preprocess.py script.
"""

#Takes stuff from excel
def from_excel(dframe, sheet_num):
    return pd.read_excel(dframe, sheet_num)

#Takes stuff from .pickle files.
def read_processed_data(fname='data/processed/processed.pickle'):
    dframe = pd.read_pickle(fname)
    return dframe

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

    conjoined = pd.merge(left=dframe, right=dframe2.loc[dframe2['year'] > 2004], how='left', on=['country', 'year'])
    #drop any rows without one of the 3 columns
    #conjoined = conjoined.dropna(subset=['Social support', 'GINI index (World Bank estimate)', 'Total Taxes'])
    conjoined_final = conjoined[['country', 'year', 'Social support', 'GINI index (World Bank estimate)', 'Total Taxes']]
    conjoined_final.to_pickle(output_file)
    if excel is not None:
        conjoined_final.to_excel(excel)
if __name__ == '__main__':
    main()