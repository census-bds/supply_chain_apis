import pandas as pd

from data_source import Api
from config import CENSUS_API_KEY
from bs4 import BeautifulSoup as bs
import pandas as pd 
import io
import openpyxl
import requests
import os 

class QPC(Api):
    def __init__(self):
        super().__init__()
        self.file_path = 'data/QPC/'

    def generate_urls(self, years=[2022, 2021]): 
        urls = []
        for year in years: 
            url = f"https://www2.census.gov/programs-surveys/qpc/tables/{year}/"
            tables = requests.get(url)
            soup = bs(tables.content)

            href_soup = soup.find_all('a', href=True)
            for a in href_soup: 
                if ".xlsx" in a['href']: 
                    extracted_url = url + a['href']
                    urls.append((a['href'], extracted_url))
        return urls
    
    def clean_qpc_file(self, urls): 
        dfs = []
        new_unnamed = "Industry Coverage LT 50p"
        unnamed = {
            "Unnamed: 2": new_unnamed, 
            "Unnamed: 5": new_unnamed, 
            "Unnamed: 7": new_unnamed
        }
        header_sheet_configs = {
            "FULL Utilization Rates": (4, "A:L"), 
            "EMERGENCY Utilization Rates": (4, "A:H")
        }
        # enumerate allows us to look at tuples 
        for (label, url) in urls: 
            content = requests.get(url).content
            print("url: ", url)
            xl = pd.ExcelFile(content, engine = "openpyxl")

            for name in xl.sheet_names: 
                if name in header_sheet_configs: 
                    df = pd.read_excel(
                        xl, 
                        name, 
                        header = header_sheet_configs[name][0], 
                        usecols = header_sheet_configs[name][1], 
                        true_values = ['c']
                    ) 
                    df = df.rename(columns = unnamed)
                    df[new_unnamed] = df[new_unnamed].fillna(False)
                    df = df.replace('c', True)
                    
                    dfs.append((label, df))
                    self.download_qpc_file(name, label, df)
        return dfs

    def download_qpc_file(self, sheet, label, df): 
        new_filename = sheet.replace(" ", "_") + "_" + label 
        new_filename = new_filename.replace(".xlsx", ".csv")
        if not os.path.exists(self.file_path): 
            os.makedirs(self.file_path)
        
        file_path = self.file_path + new_filename
        
        return df.to_csv(file_path)
    

