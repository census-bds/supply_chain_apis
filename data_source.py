import pandas as pd
import requests
import csv
from config import CENSUS_API_KEY
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
        self.url = BASE_URL_CENSUS
        self.file_path = 'data/'

    def get_request(self, url):
        return requests.get(url).json(strict=False)

    def write_csv(self, output, file_name): 
        pd.DataFrame(output[1:], columns=output[0]).to_csv(
            self.file_path + file_name, index=False
        )
        return


    # def pull_by_commodity(self):
    #     pass


class IntlTrade(Api):
    def __init__(self):
        super().__init__()
        self.file_path = 'data/Intl Trade/'

    def state_lookup(self, exports=True, year=2022):
        url = self.url + \
            'timeseries/intltrade/{}/statehs?get=STATE,{}_COMMODITY,{}_COMMODITY_LDESC,{}_VAL_MO&YEAR={}&MONTH=12&COMM_LVL=HS6&key={}'.format(
                'exports' if exports else 'imports',
                'E' if exports else 'I',
                'E' if exports else 'I',
                'ALL' if exports else 'GEN',
                year, 
                CENSUS_API_KEY
            )
        print(url)
        return self.get_request(url)
    
    def export_all(self):
        #self.write_csv(self.state_lookup(year=2021), 'state_hs_exports_2021.csv')
        self.write_csv(self.state_lookup(exports=False, year=2021), 'state_hs_imports_2021.csv')
        return

class EconomicCensus(Api):
    def __init__(self):
        super().__init__()

    def remove_d_flag(self, data):
        df = pd.DataFrame(data[1:], columns=data[0])
        flag_cols = [col for col in df if col[-2:] == "_F"]
        for col in flag_cols:
            df[col[:-2]] = df.apply(
                lambda x: None if x[col] == 'D' else x[col[:-2]], axis=1
            )
        df.drop(columns=flag_cols, inplace=True)
        return [list(df.columns)] + df.values.tolist()


    def naics_lookup(self):
        url = self.url + "2017/ecnbasic?get=FIRM,FIRM_F,ESTAB,ESTAB_F&for=state:*&NAICS2017=*&key={}".format(
            CENSUS_API_KEY
        )
        print(url)
        return self.get_request(url)
        # return self.remove_d_flag(self.get_request(url))
