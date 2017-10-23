import click
import seaborn as sea
import sys

sys.path.append('..')
from src.data import read_processed_data

#NEEDS TO BE GENERALIZED
def exploratory_visualization(dframe):
    return sea.pairplot(dframe, vars=['x0', 'x1', 'x2', 'x3'], hue='y')

def kMeansFigures(count):
    for cluster in range(2, count):
        print("fuck")


 #Read data from an input csv and output it into a png.
@click.command()
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False))
@click.argument('output_file', type=click.Path(writable=True, dir_okay=False))
def main(input_file, output_file):
    print('Graphing the pairwise dist')

    dframe = read_processed_data(input_file)
    graph = exploratory_visualization(dframe)
    graph.savefig(output_file)

if __name__ == '__main__':
    main()