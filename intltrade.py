import requests
import pandas as pd
from data_source import Api
from exceptions import RequestBlankException
from config import CENSUS_API_KEY

class IntlTrade(Api):
    def __init__(self):
        super().__init__()
        self.file_path = 'data/Intl Trade/'

    #TO DO: add up the weights by all the different mode of transit types

    def schedule_d(self):
        # Grabs and cleans the schedule D file and returns a dataframe of port codes and their names
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

    def geo_hs_lookup(self, geo=None, hs='HS6', exports=True, year=2021, datetype='year'):
        '''
        Grabs total value of shipments for the year.
        Inputs:
        geo: either 'state' or 'port' or None. None will grab nationwide values.
        hs: The HS level to split on. Options are 'HS2', 'HS4', or 'HS6'
        exports: True if exports, False if imports
        year: the year to pull
        '''
        url = self.url + \
            'timeseries/intltrade/{}/{}hs?get={}{}_COMMODITY,{}_VAL_{}&YEAR={}&MONTH={}&COMM_LVL={}&key={}'.format(
                'exports' if exports else 'imports',
                geo if geo else '',
                geo.upper() + "," if geo else "",
                'E' if exports else 'I',
                'ALL' if exports else 'GEN',
                'YR' if datetype == 'year' else 'MO',
                year,
                '12' if datetype == 'year' else '*',
                hs,
                CENSUS_API_KEY
            )
        print(url)
        return self.get_request(url)


    def combine_geo(self, geo=None, hs='HS6', years=(2020, 2021), datetype='year'):
        # Calls APIs and returns imports and exports joined and cleaned in a dataframe
        all_years = []
        for year in range(years[0], years[1] + 1):
            imp = self.geo_hs_lookup(
                geo=geo, hs=hs, exports=False, year=year, datetype=datetype
            )
            exp = self.geo_hs_lookup(
                geo=geo, hs=hs, year=year, datetype=datetype
            )
            val_suffix = 'YR' if datetype == 'year' else 'MO'
            drop_cols = ['YEAR', 'COMM_LVL', 'MONTH'] \
                if datetype == 'year' else ['YEAR', 'COMM_LVL']
            imp = pd.DataFrame(data=imp[1:], columns=imp[0]).drop(
                columns=drop_cols
            )
            imp = imp.loc[imp['GEN_VAL_{}'.format(val_suffix)] != '0']
            exp = pd.DataFrame(data=exp[1:], columns=exp[0]).drop(
                columns=drop_cols
            )
            exp = exp.loc[exp['ALL_VAL_{}'.format(val_suffix)] != '0']
            add_merge_cols = []
            if geo:
                add_merge_cols.append(geo.upper())
            if datetype == 'month':
                add_merge_cols.append('MONTH')
            combined = imp.merge(
                exp,
                left_on=['I_COMMODITY'] + add_merge_cols,
                right_on=['E_COMMODITY'] + add_merge_cols,
                how='outer'
            )
            if geo:
                combined = combined.loc[combined[geo.upper()] != "-"]
            combined['YEAR'] = year
            all_years.append(combined)
        all_years_combined = pd.concat(all_years)
        all_years_combined[hs] = all_years_combined.apply(
            lambda x: x['I_COMMODITY'] if pd.notna(x['I_COMMODITY']) else x['E_COMMODITY'],
            axis=1
        )
        all_years_combined.drop(
            columns=['I_COMMODITY', 'E_COMMODITY'], inplace=True
        )
        all_years_combined.rename(
            columns={
                'GEN_VAL_{}'.format(val_suffix): 'import_value',
                'ALL_VAL_{}'.format(val_suffix): 'export_value'
            },
            inplace=True
        )
        all_years_combined['import_value'] = all_years_combined['import_value'].apply(
            lambda x: 0 if pd.isnull(x) else x
        )
        all_years_combined['export_value'] = all_years_combined['export_value'].apply(
            lambda x: 0 if pd.isnull(x) else x
        )
        return all_years_combined

