import click
import numpy as np
import pandas as pd
from preprocess import read_processed_data, dropNA


"""
This script selects data from a dataset. It can remove categorical data, NaN entries, and certain columns.

CALLING THIS FILE: data_selector $< $@ #x #y #z --trimna=False --trimcat=False --excel PATH

UNFINISHED: Cannot remove all numerical data
"""

@click.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('output_file', type=click.Path(writable=True, dir_okay=False))
@click.argument('cols', nargs=-1)#numeric locations of desired columns. Format: x y z
@click.option('--trimna', default=False)#Trims NaN (and 0) entries.
@click.option('--trimcat', default=False) #Trim Categorical Data. Preserves data in column 00, expecting it to be a category.
@click.option('--excel', type=click.Path(writable=True, dir_okay=False))
def main(input_file, output_file, cols, trimna, trimcat, excel):
    dframe = read_processed_data(input_file)

    numericCols = [int(i) for i in list(cols)] #Turns the "cols" tuple argument into a list of integers.
    if len(cols) > 1:
        dframe = dframe.iloc[:, numericCols]
    if trimna:
        dframe = dropNA(dframe)
    if trimcat:
       dframe.iloc[:, 1:] = dframe.iloc[:, 1:].select_dtypes(include=[np.number])

    dframe.to_pickle(output_file)
    if excel is not None:
        dframe.to_excel(excel)
if __name__ == '__main__':
    main()
