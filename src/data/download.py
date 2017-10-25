#We use make to call this command easily. It is currently set to install "iris.csv". The dled file
#can be altered by changing the target url in that file. C&Ping it & changing url for more files.
import requests
import click
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
#click is a package that makes creating understandable command line statements easy. It allows us to
#use make to download files.
#
@click.command()
@click.argument('url')
@click.argument('filename', type=click.Path())
#@click.option('--blob')
def download_file(url, filename, blob, element):
    # if blob == 0:
        print('Downloading from URL: {} to DIRECTORY: {}'.format(url, filename))
        reply = requests.get(url)
        #"wb" indicates that we are 'writing' in 'binary' here.
        with open(filename,  'wb') as openFile:
            openFile.write(reply.content)
#ensures we are executing as the main function, rather than being imported from another module.

#BLOB DOWNLOAD SUPPORT: WEB SCRAPING
    # #Some files are saved as blobs. This is annoying, but solvable. When downloading a blob, simply provide the page URL and element of the attached download button.
    # if blob == 1:
    #     print('Downloading from URL: {} to DIRECTORY: {}'.format(url, filename))
    #     reply = requests.get(url)
    #     page = BeautifulSoup(reply.content, "lxml")
    #     print(page.prettify())
    #     parseURI = urlparse(url)
    #     print(element)
    #     #URLs are parsed as modified N-tuples. We will grab the scheme (ex: https) and netloc (ex: stackoverflow.com) and format them correctly.
    #     formattedURI = '{uri.scheme}://{uri.netloc}'.format(uri=parseURI)
    #     print(formattedURI)
    #     grab = page.find('a', {"download": element})
    #     if len(grab['href']) > 1:
    #         final_download_url = formattedURI + grab['href'] #grab the download link
    #         print(final_download_url)
    #     csv = requests.get(final_download_url)
    #     #with open(filename, 'wb') as openFile:
    #         #openFile.write(csv.content)
    #

if __name__ == '__main__':
   download_file()

