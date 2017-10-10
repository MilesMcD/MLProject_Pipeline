#We use make to call this command easily. It is currently set to install "iris.csv". The dled file
#can be altered by changing the target url in that file. C&Ping it & changing url for more files.
import requests
import click
@click.command()
@click.argument('url')
@click.argument('filename', type=click.Path())
def download_file(url, filename):
   print('Downloading from {} to {}'.format(url, filename))
   response = requests.get(url)
   with open(filename,  'wb') as ofile:
       ofile.write(response.content)
if __name__ == '__main__':
   download_file()