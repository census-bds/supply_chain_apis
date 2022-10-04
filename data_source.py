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

    def clean_api_text(self, api_text):
        api_rows = api_text.split('\n')
        api_rows[0] = api_rows[0][2:-2]
        for i in range(1, len(api_rows) - 1):
            api_rows[i] = api_rows[i][1:-2]
        api_rows[-1] = api_rows[-2][1:-2]
        api_rows = [x.split('","') for x in api_rows]
        for i in range(len(api_rows)):
            api_rows[i] = [val.replace('"', '') for val in api_rows[i]]
        return api_rows

    def get_request(self, url):
        resp = requests.get(url).text
        assert resp, "Invalid response"
        return self.clean_api_text(resp)

    def write_csv(self, output, file_name): 
        with open(self.file_path + file_name, 'w') as f:
            writer = csv.writer(f)
            for row in output:
                writer.writerow(row)
        return


    # def pull_by_commodity(self):
    #     pass


class IntlTrade(Api):
    def __init__(self):
        super().__init__()
        self.file_path = 'data/Intl Trade/'

    def state_lookup(self, exports=True, year=2022):
        url = self.url + \
            'timeseries/intltrade/{}/statehs?get=STATE,E_COMMODITY,E_COMMODITY_LDESC,{}_VAL_MO&YEAR={}&MONTH=12&COMM_LVL=HS6&key={}'.format(
                'exports' if exports else 'imports', 'ALL' if exports else 'GEN', year, CENSUS_API_KEY
            )
        print(url)
        return self.get_request(url)

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
        return self.remove_d_flag(self.get_request(url))
