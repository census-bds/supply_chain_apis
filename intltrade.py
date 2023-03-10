import requests
import pandas as pd
import data_source
from exceptions import RequestBlankException
from config import CENSUS_API_KEY, STATE_GEOID_CROSSWALK

class IntlTrade(data_source.Api):
    def __init__(self):
        super().__init__()
        self.name = "International Trade"
        self.file_path = 'data/Intl Trade/'
        self.available_vars = self.populate_vars(['label'])
        self.attributes = False
        self.state_geoid_xwalk = None

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
    
    def lookup(self, endpoint, params):
        dfs = super().lookup(endpoint, params)
        return [self.add_geo(df) for df in dfs]

    def add_geo(self, df):
        if not isinstance(self.state_geoid_xwalk, pd.DataFrame):
            self.state_geoid_xwalk = pd.read_csv(STATE_GEOID_CROSSWALK)
        geo_col = None
        if 'STATE' in df.columns:
            df = df.merge(
                self.state_geoid_xwalk[['GEO_ID', 'STATE']], on='STATE'
            )
            geo_col = 'STATE'
        #Making a custom GEO_ID for ports that is "PORT" plus the port code
        if 'PORT' in df.columns:
            df['GEO_ID'] = df['PORT'].apply(lambda x: 'PORT' + str(x))
            geo_col = 'PORT'
        if geo_col:
            df.loc[df[geo_col] == "-", "GEO_ID"] = "0100000US"
            df.drop(columns=[geo_col], inplace=True)
            df['GEO_LVL'] = geo_col
        else:
            df['GEO_ID'] = "0100000US"
            df['GEO_LVL'] = None
        return df
    
    def rename_hs_columns(self, dfs):
        for df in dfs:
            hs_cols = [col for col in df.columns if '_COMMODITY' in col]
            for col in hs_cols:
                df.rename(columns={col: 'HS'}, inplace=True)
        return dfs

    def clean_combine_dfs(self, dfs):
        #Somewhat custom function for SCIP which will merge all dfs into one and rename columns
        dfs = self.rename_hs_columns(dfs)
        join_cols = ['HS', 'COMM_LVL', 'time', 'GEO_ID']
        main_df = dfs[0]
        for df in dfs[1:]:
            join_on = [
                col for col in join_cols \
                    if col in main_df.columns and col in df.columns
            ]
            main_df = main_df.merge(df, on=join_on, how='outer')
        return main_df

