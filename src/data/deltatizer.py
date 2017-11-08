import click
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
import sys
from scipy.stats import pearsonr
"""
This function is searching for the two years with the most available 

"""

def from_excel(dframe, sheet_num):
        return pd.read_excel(dframe, sheet_num)


#Citing: https://stackoverflow.com/questions/25571882/pandas-columns-correlation-with-statistical-significance toto_tico
def calculate_pvalues(df):
    df = df.dropna()._get_numeric_data()
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in df.columns:
        for c in df.columns:
            pvalues[r][c] = round(pearsonr(df[r], df[c])[1], 15)
    return pvalues

@click.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('output_file', type=click.Path(writable=True, dir_okay=False))
@click.option('--excel', type=click.Path(writable=True, dir_okay=False))
@click.option('--fromexcel', default=-1) #variable represents sheet number. Zero base
def main(input_file, output_file, excel, fromexcel):

    if fromexcel > -1:
        dframe = pd.from_excel(input_file, fromexcel)
    else:
        dframe = pd.read_pickle(input_file)
    #normalize taxrate
    for i in range(2, len(dframe.columns)):
        curr_col = dframe.columns[i]
        dframe[curr_col] = dframe[curr_col].apply(lambda x: (x - dframe[curr_col].mean()) /
                                                                      (dframe[curr_col].max() - dframe[
                                                                          curr_col].min()))


    dframe_pre = dframe.replace(0, float('nan'))
    dframe_pre = dframe_pre.dropna()
    dframe_pre.hist()
    #print some info about the pre-differentiated frame.
    # np.set_printoptions(threshold=sys.maxsize)
    # print(dframe_pre['country'].unique())
    # print(len(dframe_pre['country'].unique()))
    # print(dframe_pre['country'].value_counts()[0:20])
    # print(dframe_pre['country'].value_counts()[21:40])
    # print(dframe_pre['country'].value_counts()[41:60])
    # print(dframe_pre['country'].value_counts()[61:80])
    # print(dframe_pre['country'].value_counts()[81:104])
    #plt.show()
    scatter_matrix(dframe, alpha=0.2, figsize=(6, 6), diagonal='kde')
    #plt.show()
    #Correlation plot
    rho = dframe_pre.corr()

    print("pre-diff correlation:")
    print(rho)

    #print(calculate_pvalues(dframe_pre))
    #calculate_pvalues(dframe_pre).to_excel("data/processed/HGSTpVal.xlsx")
    # index by country so we can target slices.
    index_countries = dframe.set_index([dframe.columns[0]])
    ##Divide the dataset into slices for differentiation.
    for i in range(len(index_countries.index.unique())):
        index_countries.loc[index_countries.index.unique()[i], index_countries.columns[1]:] = index_countries.loc[
                                                                    index_countries.index.unique()[i], index_countries.columns[1]:] \
            .diff()
    # Fix index
    dframe = index_countries.reset_index()

    #Remove rows without full data
    dframe = dframe.replace(0, float('nan'))
    dframe = dframe.dropna()
    dframe.hist()
    #plt.show()
    scatter_matrix(dframe, alpha=0.2, figsize=(6, 6), diagonal='kde')
    #plt.show()
    #correlation plot
    print("Post-diff correlation")
    rho = dframe.corr()
    print(rho)

    #print(calculate_pvalues(dframe))
    #calculate_pvalues(dframe).to_excel("data/processed/HGSTpValDiff.xlsx")
    if excel is not None:
       dframe.to_excel(excel)
    #dframe.to_pickle(output_file)

if __name__ == '__main__':
    main()
