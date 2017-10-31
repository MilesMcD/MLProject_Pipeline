import click
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

@click.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('output_file', type=click.Path(writable=True, dir_okay=False))
@click.option('--excel', type=click.Path(writable=True, dir_okay=False))
@click.option('--fromexcel', default=-1) #variable represents sheet number. Zero base
def main(input_file, output_file, excel, fromexcel):
    print("hello")
    if excel is not None:
        x.to_excel(excel)


if __name__ == '__main__':
    main()