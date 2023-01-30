import pandas as pd
import requests
import datetime
import yaml
import logging
from exceptions import TooManyFields, RequestBlankException, FutureYearException, InvalidSurveyYear, UnknownDataSource
from urls import BASE_URL_CENSUS
from config import CENSUS_API_KEY

with open('api_endpoints.yml', 'r') as file:
    API_ENDPOINTS = yaml.safe_load(file)

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
        self.available_vars = {}
        self.geographies = {}
        self.attributes = True

    def lookup_all(self):
        endpoint_dict = API_ENDPOINTS[self.name]
        dfs = []
        for endpoint, params in endpoint_dict.items():
            if params:
                dfs.append(self.lookup(endpoint, params))
        return dfs

    def lookup_subfields(self, endpoint, params):
        url = self.url + endpoint + "?"
        param_strings = []
        for param, values in params.items():
            param_strings.append(param + "=" + ",".join(values))
        url += "&".join(param_strings)
        print(url)
        return self.get_request(url)

    def lookup(self, endpoint, params):
        #TO DO: split the lookup if more than 50 fields requested
        fields = params['get']
        if not params.get('key'):
            params['key'] = [CENSUS_API_KEY]
        available_fields = list(self.available_vars.get(endpoint).keys())
        assert available_fields, endpoint + " is not available."
        if not fields:
            fields = available_fields
        fields_to_use = []
        for field in fields:
            if field in available_fields:
                fields_to_use.append(field)
                if self.attributes:
                    attributes = self.available_vars.get(
                        endpoint
                    )[field]['attributes']
                    if attributes:
                        fields_to_use.append(attributes)
            else:
                logging.warning(
                    "{} is not an available field for endpoint {}".format(
                        field, endpoint
                    )
                )
        if len(fields_to_use) > 49:
            raise TooManyFields
        else:
            params['get'] = fields_to_use
            return self.lookup_subfields(endpoint, params)
    
    def populate_vars(self, fields_needed):
        def _lookup_vars(endpoint):
            variables = requests.get(
                BASE_URL_CENSUS + endpoint + "/variables.json"
            ).json()
            var_dict = {}
            for variable, variable_dict in variables['variables'].items():
                if variable == variable.upper():
                    var_dict[variable] = {}
                    for field in fields_needed:
                        var_dict[variable][field] = variable_dict.get(field)
            return var_dict #Kind of hacky. There are some non-variables that are lowercase so we use that to get rid of them.
        endpoints = API_ENDPOINTS.get(self.name)
        if not endpoints:
            raise UnknownDataSource(self.name)
        available_vars = {}
        for endpoint in endpoints:
            available_vars[endpoint] = _lookup_vars(endpoint)
        return available_vars

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

    # def check_vars(self, endpoint):
    #     if not self.availale_vars.get(endpoint):
    #         self.availale_vars[endpoint] = [
    #             col for col in self.get_request(
    #                 'https://api.census.gov/data/{}/variables.json'.format(endpoint)
    #             )['variables'].keys() if not col in ['for', 'in', 'ucgid']
    #         ]

    def get_request(self, url):
        r = requests.get(url)
        if r.text:
            try:
                data = r.json(strict=False)
            except:
                raise Exception(r.text)
            return pd.DataFrame(data[1:], columns=data[0])
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

class Survey(Api):
    def __init__(self):
        super().__init__()

    def remove_flag(self, df, flag_types):
        flag_cols = [col for col in df if col[-2:] == "_F"]
        for col in flag_cols:
            df[col[:-2]] = df.apply(
                lambda x: None if x[col] in flag_types else x[col[:-2]], axis=1
            )
        df.drop(columns=flag_cols, inplace=True)
        return df

    def lookup_subfields(self, endpoint, geo_id=True):
        return self.remove_flag(
            super().lookup_subfields(endpoint),
            ["D", "X"]
        )

