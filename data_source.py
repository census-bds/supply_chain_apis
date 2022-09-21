import pandas as pd
import requests
from config import CENSUS_API_KEY
from urls import BASE_URL_CENSUS

class DataSource():
    def most_recent_naics(self, naics):
        # Harmonizes naics to the most recent version
        return

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

    def naics_lookup(self, exports=True, year=2022):
        url = self.url + 'timeseries/intltrade/{}/statenaics?get=STATE,NAICS,ALL_VAL_YR&YEAR=2021&key={}'.format(
            'exports' if exports else 'imports', CENSUS_API_KEY
        )
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
        url = self.url + "2017/ecnbasic?get=ESTAB,ESTAB_F&for=state:*&NAICS2017=*&key={}".format(
            CENSUS_API_KEY
        )
        
        return self.remove_d_flag(self.get_request(url))
