import pandas as pd
import requests
from exceptions import RequestBlankException
from urls import BASE_URL_CENSUS

class DataSource():

    def most_recent_naics(self, naics, year):
        # Harmonizes naics to the most recent version
        return

    def product_hs_code(self, code, code_type):
        # Harmonizes product codes to the most recent HS
        return
    pass

class Api(DataSource):
    def __init__(self):
        super().__init__()
        self.url = BASE_URL_CENSUS
        self.file_path = 'data/'

    def get_request(self, url):
        r = requests.get(url)
        if r.text:
            return r.json(strict=False)
        else:
            raise RequestBlankException(url)

    def write_csv(self, output, file_name): 
        '''
        Output: a list of lists, it's what the _lookup functions return
        File_name: string with a path
        '''
        pd.DataFrame(output[1:], columns=output[0]).to_csv(
            self.file_path + file_name, index=False
        )
        return








class CountyBusinessPatterns(Api):
    def __init__(self):
        super().__init__()
        self.file_path = 'data/CBP/'
    
    def county_lookup(self):
        url = self.url + "2020/cbp?get=GEO_ID,ESTAB,NAICS2017_LABEL,NAME&for=COUNTY:*&NAICS2017=*&key={}".format(
            CENSUS_API_KEY
        )
        return self.get_request(url)

