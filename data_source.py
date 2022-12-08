import pandas as pd
import requests
import datetime
from exceptions import RequestBlankException, FutureYearException, InvalidSurveyYear
from urls import BASE_URL_CENSUS

class DataSource():
    def __init__(self):
        self.name = ''

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

    def check_year(self, year, cadence, mod):
        '''
        Checks if they year being requested is valid based on whether it is in
        the future and whether data exists for that year.
        year (int): the year to check
        cadence (int): the regularity of data availability. (i.e. every 2 years)
        mod (int): the expected mod of year / cadence. (i.e. econ census is done
        2012, 2017, etc. so mod should be 2)
        '''
        if year > datetime.date.today().year:
            raise FutureYearException(year)
        if year % cadence != mod:
            raise InvalidSurveyYear(self.name, year)

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

