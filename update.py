import zipfile
from io import BytesIO

import requests

url = 'https://download.geonames.org/export/zip/allCountries.zip'


# download raw data from geonmaes.org
def download_and_unzip():
    print(f'Going to download {url}')
    req = requests.get(url)
    print('Download Completed, unzipping ...')
    zippy = zipfile.ZipFile(BytesIO(req.content))
    zippy.extractall('data')
    print('Unzipping done.')


if __name__ == '__main__':
    download_and_unzip()
