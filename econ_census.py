import pandas as pd
import data_source
from config import CENSUS_API_KEY

class EconomicCensus(data_source.Api):
    def __init__(self):
        super().__init__()
        self.name = "Economic Census"        
        self.available_vars = self.populate_vars()

    def remove_flag(self, data, flag_types):
        df = pd.DataFrame(data[1:], columns=data[0])
        flag_cols = [col for col in df if col[-2:] == "_F"]
        for col in flag_cols:
            df[col[:-2]] = df.apply(
                lambda x: None if x[col] in flag_types else x[col[:-2]], axis=1
            )
        df.drop(columns=flag_cols, inplace=True)
        return [list(df.columns)] + df.values.tolist()


class EcnBasic(EconomicCensus):
    def __init__(self):
        super().__init__()
    
    def ecnbasic_lookup(self, geo=None, year=2017):
        self.check_year(year, 5, 2)
        self.check_vars(year)
        
        variables = ['FIRM', 'FIRM_F', 'RCPTOT', 'RCPTOT_F', 'ESTAB', 'ESTAB_F']
        variables = [
            col for col in variables if col in \
                self.availale_vars['ecnbasic'][year]
        ]
        url = self.url + "{}/ecnbasic?get=GEO_ID,{}{}&for={}&NAICS{}=*&key={}".format(
            year,
            geo.upper() + "," if geo else '',
            ','.join(variables),
            '{}:*'.format(geo) if geo else 'us',
            year,
            CENSUS_API_KEY
        )
        print(url)
        return self.remove_flag(self.get_request(url), flag_types=["D", "X"])

class EcnSize(EconomicCensus):
    def __init__(self):
        super().__init__()

    def naics_size_lookup(self):
        url = self.url + "2017/ecnsize?get=CONCENFI,CONCENFI_LABEL,HHI,HHI_F,NAICS2017_LABEL,ESTAB,RCPTOT&for=us:1&NAICS2017=*&key={}".format(
            CENSUS_API_KEY
        )
        print(url)
        return self.remove_flag(self.get_request(url), flag_types=["D", "X"])