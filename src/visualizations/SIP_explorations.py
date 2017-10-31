import click
import sys
from sklearn.metrics import silhouette_samples, silhouette_score

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D #this is necessary.
sys.path.append('..')
from src.data import read_processed_data

"""
This script is being used to look at interpolation information in the happiness report. 

"""

@click.command()
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False))
@click.argument('output_file', type=click.Path(writable=True, dir_okay=False))
@click.option('--secondfile', type=click.Path(writable=True, dir_okay=False), default='a')
#Currently set to do interpolation graphs.

def main(input_file, output_file, secondfile):
    print('Graphing')

    dframe = read_processed_data(input_file)
    if len(secondfile) > 1:
        dframe2 = read_processed_data(secondfile)

        f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
       #Time period we are investigating
        begin = 0
        end = 12
        ax1.set_title("Non-Interpolated")
        ax1.set_xlabel("Years")
        ax1.set_ylabel("Normalized Social Support")
        for i in range(5):
            line, = ax1.plot(dframe2.iloc[begin:end, 1], dframe2.iloc[begin:end, 5], label=dframe2.iloc[begin, 0])
            #line.set_label
            begin += 12
            end += 12
        begin = 0
        end = 12
        ax2.set_title("Interpolated")
        ax2.set_xlabel("Years")
        ax1.set_ylabel("Normalized Social Support")
        for i in range(5):
            ax2.plot(dframe.iloc[begin:end, 1], dframe.iloc[begin:end, 5], label=dframe.iloc[begin, 0])
            begin += 12
            end += 12
    else:
        plt.plot(dframe.iloc[14:23, 1], dframe.iloc[14:23, 5])
    ax1.legend()
    ax2.legend()
    plt.show()
    f.savefig(output_file)
if __name__ == '__main__':
    main()