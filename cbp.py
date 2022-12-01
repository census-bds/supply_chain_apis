from data_source import Api
from config import CENSUS_API_KEY

class CountyBusinessPatterns(Api):
    def __init__(self):
        super().__init__()
        self.file_path = 'data/CBP/'
    
    def county_lookup(self):
        url = self.url + "2020/cbp?get=GEO_ID,ESTAB,NAICS2017_LABEL,NAME&for=COUNTY:*&NAICS2017=*&key={}".format(
            CENSUS_API_KEY
        )
        return self.get_request(url)