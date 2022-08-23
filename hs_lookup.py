import pandas as pd
import requests
from config import CENSUS_API_KEY
from urls import BASE_URL_CENSUS, INTL_TRADE
from api_utils import clean_api_text


FTD_URL = BASE_URL_CENSUS + INTL_TRADE

def hs_lookup(hs_code, exports=True, year=2022):
    url = FTD_URL + 'exports' if exports else 'imports'
    url += '/hs?get=ALL_VAL_YR,QTY_1_MO,QTY_1_MO_FLAG&time={}&COMM_LVL=HS4&E_COMMODITY={}&key={}'.format(
        year, hs_code, CENSUS_API_KEY
    )
    resp = requests.get(url).text
    assert resp, "Invalid response"
    return clean_api_text(resp)

def naics_lookup(naics, exports=True, year=2022):
    url = FTD_URL + 'exports' if exports else 'imports'
    url += '/naics?get=ALL_VAL_YR&time=2022&NAICS={}&key={}'.format(
        naics, CENSUS_API_KEY
    )
    resp = requests.get(url).text
    assert resp, "Invalid response"
    return clean_api_text(resp)