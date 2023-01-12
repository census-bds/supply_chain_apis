import pandas as pd
import requests
import datetime
import yaml
from exceptions import RequestBlankException, FutureYearException, InvalidSurveyYear, UnknownDataSource
from urls import BASE_URL_CENSUS

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

