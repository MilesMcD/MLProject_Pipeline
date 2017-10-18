#We use make to call this command easily. It is currently set to install "iris.csv". The dled file
#can be altered by changing the target url in that file. C&Ping it & changing url for more files.
import requests
import click
#click is a package that makes creating understandable command line statements easy. It allows us to
#use make to download files.
#
@click.command()
@click.argument('url')
@click.argument('filename', type=click.Path())
def download_file(url, filename):
   print('Downloading from URL: {} to DIRECTORY: {}'.format(url, filename))
   reply = requests.get(url)
   #"wb" indicates that we are 'writing' in 'binary' here.
   with open(filename,  'wb') as openFile:
       openFile.write(reply.content)
#ensures we are executing as the main function, rather than being imported from another module.
if __name__ == '__main__':
   download_file()

