import os
import requests
from io import BytesIO
from zipfile import ZipFile

import pandas as pd

from congresso_em_texto.preprocessing import ParlamentarianPreprocessor
from congresso_em_texto.utils.constants import URLS


class ParliamentarianCollector:
    def __init__(self, start_date, end_date):
        years = range(start_date.year - 3, end_date.year + 1)
        years = [year for year in years if ((year - 2) % 4 == 0)]

        self.years = years
        self.data = pd.DataFrame()
        self.preprocessor = ParlamentarianPreprocessor()

        self.model = {
            "id_parlamentar": None,
            "nome": None,
            "nome_candidatura": None,
            "cargo": None,
            "uf": None,
            "legislatura": None,
            "partido": None,
            "sigla_partido": None,
            "reeleicao": None,
        }

    def start_requests(self):
        for year in self.years:
            response = requests.get(URLS.get_candidates_url(year))

            if response.ok:
                dataset = self.extract_dataset(response)
                self.data = pd.concat([self.data, dataset])
                print(f"Coletando dados sobre os parlamentares eleitos em {year}...")

        self.data = self.preprocessor.fix(data=self.data)

    def extract_dataset(self, response):
        zipfile = ZipFile(BytesIO(response.content))
        filename = [fn for fn in zipfile.namelist() if fn.endswith("BRASIL.csv")]
        file = zipfile.open(filename[0])

        dataset = pd.read_csv(file, encoding="latin1", sep=";", low_memory=False)

        return dataset

    def save_data(self, house, filepath):
        position = "Senador(a)" if house == "senate" else "Deputado(a) Federal"
        indexes = self.data["cargo"] == position
        dataset = self.data[indexes]

        if os.path.exists(filepath):
            previous_dataset = pd.read_csv(filepath)
            dataset = pd.concat([dataset, previous_dataset])

        dataset.to_csv(filepath, encoding="utf-8", index=False)
