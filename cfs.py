from data_source import Api
from config import CENSUS_API_KEY

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