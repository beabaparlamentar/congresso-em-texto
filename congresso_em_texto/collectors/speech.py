import os
import re

from w3lib import html
from scrapy import Spider, Request

import pandas as pd

from congresso_em_texto.preprocessing import SpeechPreprocessor
from congresso_em_texto.utils.constants import SELECTORS, PATTERNS

class SpeechCollector(Spider):
    """
    Spider para coletar e processar discursos de um órgão legislativo.
    """

    name = "speech-collector"

    def __init__(
        self,
        house,
        origin,
        start_date,
        end_date,
        events_filepath,
        speeches_directory,
        *args,
        **kwargs,
    ):
        """
        Inicializa o ColetorDiscursos.

        Args:
            house (str): A casa legislativa ("senate" ou "chamber").
            origin (str): A origem dos dados.
            start_date (str): A data de início para coletar discursos (AAAA-MM-DD).
            end_date (str): A data de término para coletar discursos (AAAA-MM-DD).
            events_filepath (str): Caminho para o arquivo CSV de eventos.
            speeches_directory (str): Diretório para salvar os discursos.
            *args: Argumentos adicionais.
            **kwargs: Argumentos adicionais.
        """
        super(SpeechCollector, self).__init__(*args, **kwargs)

        events = pd.read_csv(events_filepath)
        events["data"] = pd.to_datetime(events["data"], format="%Y-%m-%d")
        events = events.query("@start_date <= data <= @end_date")

        self.house = house
        self.origin = origin
        self.start_date = start_date
        self.end_date = end_date
        self.directory = speeches_directory
        self.events = events.drop_duplicates()
        self.preprocessor = SpeechPreprocessor()

        self.model = {
            "id_evento": None,
            "ordem_discurso": None,
            "orador": None,
            "texto": None,
        }

    def start_requests(self):
        """
        Gera as primeiras requisições para coletar discursos com base na casa selecionada.

        Yields:
            Request: Uma requisição para coletar discursos.
        """ 
        if self.house == "senate":
            pass
        if self.house == "chamber":
            return self.start_chamber_requests()

    def start_chamber_requests(self):
        """
        Gera requisições para coletar discursos da câmara.

        Yields:
            Request: Uma requisição para coletar discursos de um evento.
        """
        for _, row in self.events.iterrows():
            event = row.to_dict()

            yield Request(
                url=event["discursos"],
                callback=self.parse_chamber_events,
                meta={"event": event},
            )

    def parse_chamber_events(self, response):
        """
        Analisa eventos da câmara e extrai discursos.

        Args:
            response: A resposta da requisição HTTP.
        """
        event = response.meta.get("event")
        content_selector = SELECTORS.get(name="content")
        speaker_pattern = PATTERNS.get_regex(name="chamber_speaker")

        content = response.css(content_selector).get()
        content = html.remove_tags(content)
        content = re.split(speaker_pattern, content)[1:]

        speeches = []
        for index in range(0, len(content), 2):
            speech = {
                "orador": content[index],
                "texto": content[index + 1],
            }

            speech = self.preprocessor.fix(speech=speech)
            speeches.append(speech)

        self.save_data(speeches=speeches, event=event)

    def save_data(self, speeches, event):
        """
        Salva os dados dos discursos em um arquivo CSV.

        Args:
            speeches (list): Lista de dados dos discursos.
            event (dict): Informações do evento.
        """
        event_year = event["data"].strftime("%Y")
        event_month = event["data"].strftime("%m")
        event_id = str(event["id_evento"])

        speeches = pd.DataFrame(speeches)
        speeches["id_evento"] = event_id

        filename = self.preprocessor.get_filename(event_id)
        filepath = os.path.join(self.directory, event_year, event_month, filename)

        if os.path.exists(filepath):
            previous_dataset = pd.read_csv(filepath)
            speeches = pd.concat([previous_dataset, speeches])
            speeches = speeches.drop_duplicates(subset=["orador", "texto"])

        speeches["ordem_discurso"] = speeches.index + 1

        speeches = speeches[self.model.keys()]
        speeches.to_csv(filepath, encoding="utf-8", index=False)
        print(f"Novos discursos armazenados em: {filepath}")
