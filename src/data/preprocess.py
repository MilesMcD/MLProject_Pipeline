import click
import pandas as pd
#USE --EXCEL AFTER CALL TO GET CSV IN THAT FORMAT. STANDARD IN MAKEFILE.

#return features
def get_features(dframe):
    return dframe[['x0', 'x1', 'x2', 'x3']]

#return labels
def get_label(dframe):
    return dframe['y']

#read in raw data
def read_raw_data(fname='src/data/raw/iris.csv'):
    dframe = pd.read_csv(fname, header=None)
    return dframe

#rename labels
def preprocess_data(dframe):
    dframe = dframe.copy()  #create new frame to ensure safety of operation.
    dframe.columns = ['x0', 'x1', 'x2', 'x3', 'y']
    return dframe

#read a processed frame.
def read_processed_data(fname='data/processed/processed.pickle'):
    dframe = pd.read_pickle(fname)
    return dframe

#main method: if this file is called alone, this is will be called. processes data.
@click.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('output_file', type=click.Path(writable=True, dir_okay=False))
@click.option('--excel', type=click.Path(writable=True, dir_okay=False))
def main(input_file, output_file, excel):
    print('Preprocessing data')

    dframe = read_raw_data(input_file)
    dframe = preprocess_data(dframe)

    dframe.to_pickle(output_file)
    if excel is not None:
        dframe.to_excel(excel)


if __name__ == '__main__':
    main()