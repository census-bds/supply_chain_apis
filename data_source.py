import pandas as pd
import requests
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
        super().__init__()
        self.url = BASE_URL_CENSUS
        self.file_path = 'data/'

    def get_request(self, url):
        return requests.get(url).json(strict=False)

    def write_csv(self, output, file_name): 
        '''
        Output: a list of lists, it's what the _lookup functions return
        File_name: string with a path
        '''
        pd.DataFrame(output[1:], columns=output[0]).to_csv(
            self.file_path + file_name, index=False
        )
        return



class IntlTrade(Api):
    def __init__(self):
        super().__init__()
        self.file_path = 'data/Intl Trade/'

    #TO DO: add up the weights by all the different mode of transit types

    def schedule_d(self):
        def _split_first_comma(row):
            return [row[:row.find(",")], row[row.find(",") + 1:]]
        url = "https://www.census.gov/foreign-trade/schedules/d/dist3.txt"
        sched_d = requests.get(url).text
        sched_d = sched_d.split("\n")
        sched_d = [row.replace('"', '').replace('\r', '') for row in sched_d]
        sched_d = [_split_first_comma(row) for row in sched_d]
        sched_d = [_split_first_comma(row[1]) for row in sched_d]
        return pd.DataFrame(
            data=[row for row in sched_d if row[0].isdigit()],
            columns=['port', 'port_name']
        )
# geo can be 'state', 'port', or none... will add month as parameter 
    def geo_lookup(self, geo='state', exports=True, year=2022):
        url = self.url + \
            'timeseries/intltrade/{}/{}hs?get={},{}_COMMODITY,{}_VAL_MO&YEAR={}&MONTH=12&COMM_LVL=HS6&key={}'.format(
                'exports' if exports else 'imports',
                'state' if geo == 'state' else 'port',
                'STATE' if geo == 'state' else 'PORT',
                'E' if exports else 'I',
                'ALL' if exports else 'GEN',
                year, 
                CENSUS_API_KEY
            )
        print(url)
        return self.get_request(url)


    def combine_geo(self, geo='state', years=(2020, 2021)):
        all_years = []
        for year in range(years[0], years[1] + 1):
            imp = self.geo_lookup(geo=geo, exports=False, year=year)
            exp = self.geo_lookup(geo=geo, year=year)
            imp = pd.DataFrame(data=imp[1:], columns=imp[0]).drop(
                columns=['YEAR', 'COMM_LVL', 'MONTH']
            )
            exp = pd.DataFrame(data=exp[1:], columns=exp[0]).drop(
                columns=['YEAR', 'COMM_LVL', 'MONTH']
            )
            combined = imp.merge(
                exp,
                left_on=[geo.upper(), 'I_COMMODITY'],
                right_on=[geo.upper(), 'E_COMMODITY'],
                how='outer'
            )
            combined = combined.loc[combined[geo.upper()] != "-"]
            combined['YEAR'] = year
            all_years.append(combined)
        all_years_combined = pd.concat(all_years)
        all_years_combined['HS6'] = all_years_combined.apply(
            lambda x: x['I_COMMODITY'] if pd.notna(x['I_COMMODITY']) else x['E_COMMODITY'],
            axis=1
        )
        all_years_combined.drop(
            columns=['I_COMMODITY', 'E_COMMODITY'], inplace=True
        )
        return all_years_combined.rename(
            columns={'GEN_VAL_MO': 'import_value', 'ALL_VAL_MO': 'export_value'}
        )


class EconomicCensus(Api):
    def __init__(self):
        super().__init__()
        self.file_path = 'data/Econ Census/'

    def remove_flag(self, data, flag_types):
        df = pd.DataFrame(data[1:], columns=data[0])
        flag_cols = [col for col in df if col[-2:] == "_F"]
        for col in flag_cols:
            df[col[:-2]] = df.apply(
                lambda x: None if x[col] in flag_types else x[col[:-2]], axis=1
            )
        df.drop(columns=flag_cols, inplace=True)
        return [list(df.columns)] + df.values.tolist()


    def state_naics_lookup(self):
        url = self.url + "2017/ecnbasic?get=GEO_ID,STATE,FIRM,FIRM_F,RCPTOT,RCPTOT_F,ESTAB,ESTAB_F&for=state:*&NAICS2017=*&key={}".format(
            CENSUS_API_KEY
        )
        print(url)
        return self.remove_flag(self.get_request(url), flag_types=["D", "X"])

    def naics_size_lookup(self):
        url = self.url + "2017/ecnsize?get=CONCENFI,CONCENFI_LABEL,HHI,HHI_F,NAICS2017_LABEL,ESTAB,RCPTOT&for=us:1&NAICS2017=*&key={}".format(
            CENSUS_API_KEY
        )
        print(url)
        return self.remove_flag(self.get_request(url), flag_types=["D", "X"])


class CountyBusinessPatterns(Api):
    def __init__(self):
        super().__init__()
        self.file_path = 'data/CBP/'
    
    def county_lookup(self):
        url = self.url + "2020/cbp?get=GEO_ID,ESTAB,NAICS2017_LABEL,NAME&for=COUNTY:*&NAICS2017=*&key={}".format(
            CENSUS_API_KEY
        )
        return self.get_request(url)

class Cfs(Api):
    def __init__(self):
        super().__init__()
        self.file_path = 'data/CFS/'

    def grab_cfs_areas(self):
        #Loop through all states to grab all cfs areas
        pass

    def geo_comm_lookup(self, geo="state", year=2017):
        url = self.url + "2017/cfsarea?get=NAME,GEO_ID,COMM,COMM_LABEL,VAL,TON&for={}:*&YEAR={}&key={}".format(
            "state" if geo == "state" else "cfs%20area%20(or%20part):*",
            year,
            CENSUS_API_KEY
        )
        if geo != "state":
            return self.grab_cfs_areas()
        return self.get_request(url)