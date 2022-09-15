import pandas as pd
import requests
from config import CENSUS_API_KEY
from urls import BASE_URL_CENSUS, INTL_TRADE, ASM
from api_utils import clean_api_text

class DataSource():
    pass

class Api(DataSource):
    def __init__(self):
        self.url = BASE_URL_CENSUS

    def clean_api_text(self, api_text):
        api_rows = api_text.split()
        api_rows[0] = api_rows[0][2:-2]
        for i in range(1, len(api_rows) - 1):
            api_rows[i] = api_rows[i][1:-2]
        api_rows[-1] = api_rows[-2][1:-2]
        api_rows = [x.split(',') for x in api_rows]
        for i in range(len(api_rows)):
            api_rows[i] = [val.replace('"', '') for val in api_rows[i]]
        return api_rows

    def get_request(self, url):
        resp = requests.get(url).text
        assert resp, "Invalid response"
        return self.clean_api_text(resp)

    # def pull_by_commodity(self):
    #     pass


class IntlTrade(Api):
    def __init__(self):
        super().__init__()
        self.url += "intltrade/"

    def naics_lookup(self, exports=True, year=2022):
        url = self.url + 'exports' if exports else 'imports'
        url += 'timeseries/statenaics?get=STATE,NAICS,ALL_VAL_YR&YEAR=2021&key={}'.format(
            CENSUS_API_KEY
        )
        return self.get_request(url)

class EconomicCensus(Api):
    def __init__(self):
        super().__init__()

    def naics_lookup(self):
        url = self.url + "2017/ecnbasic?get=ESTAB,ESTAB_F&for=state:*&NAICS2017=*&key={}".format(
            CENSUS_API_KEY
        )
        print(url)
        return self.get_request(url)
