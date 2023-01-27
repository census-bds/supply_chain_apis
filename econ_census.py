import pandas as pd
import data_source
from config import CENSUS_API_KEY
from exceptions import TooManyFields
import logging

class EconomicCensus(data_source.Survey):
    def __init__(self):
        super().__init__()
        self.name = "Economic Census"
        self.available_vars = self.populate_vars(['attributes'])
        self.api_params['for'] = ['state:*']
    #TO DO: HANDLE FOR CLAUSE (GEOGRAPHICAL) RESTRICTIONS



