import pandas as pd
from scrapy import Spider, FormRequest

from congresso_em_texto.preprocessing import EventPreprocessor
from congresso_em_texto.utils.constants import SELECTORS, URLS


class EventCollector(Spider):
    """
    Spider para coleta e processamento de informações sobre eventos legislativos.
    """
    name = "event-collector"

    def __init__(self, house, origin, start_date, end_date, *args, **kwargs):
        """
        Inicializa o ColetorEventos.

        Args:
            house (str): A casa legislativa ("senate" ou "chamber").
            origin (str): A origem dos dados ("plenary" ou "committee").
            start_date (str): A data de início do intervalo (AAAA-MM-DD).
            end_date (str): A data de término do intervalo (AAAA-MM-DD).
            *args: Argumentos adicionais.
            **kwargs: Argumentos adicionais.
        """
        super(EventCollector, self).__init__(*args, **kwargs)
        dates = pd.date_range(start=start_date, end=end_date).tolist()

        self.house = house
        self.origin = origin
        self.dates = dates
        self.preprocessor = EventPreprocessor()
        self.allowed_domains = URLS.get_domain_url(house)

        self.model = {
            "id_evento": None,
            "categoria_evento": None,
            "ambiente_legislativo": None,
            "categoria_ambiente": None,
            "casa_legislativa": None,
            "data": None,
            "discursos": None,
        }

    def start_requests(self):
        """
        Inicia as requisições para coletar informações sobre eventos legislativos.
        """
        if self.house == "senate":
            pass
        if self.house == "chamber":
            return self.start_chamber_requests()

    def start_chamber_requests(self):
        """
        Inicia as requisições para coletar eventos da câmara.

        Yields:
            FormRequest: Uma requisição para coletar eventos.
        """
        formatted_dates = [date.strftime("%d/%m/%Y") for date in self.dates]
        search_type = "plenario" if self.origin == "plenary" else "comissao"

        for date in formatted_dates:
            print(f"Coletando dados sobre os eventos do dia {date}...")

            yield FormRequest(
                url=URLS.get_search_url(self.house),
                method="GET",
                formdata={
                    "pageSize": "1000",
                    "CampoOrdenacao": "dtSessao",
                    "TipoOrdenacao": "ASC",
                    "basePesq": search_type,
                    "dtInicio": date,
                    "dtFim": date,
                },
                callback=self.parse_chamber_events,
            )

    def parse_chamber_events(self, response):
        """
        Analisa os eventos da câmara e extrai informações.

        Args:
            resposta: A resposta da requisição HTTP.
        """
        table_selector = SELECTORS.get(name="chamber_events")
        table = response.css(table_selector)

        if table:
            if self.origin == "plenary":
                table = table[0::2]

            for row in table:
                event = self.model.copy()
                for key in event.keys():
                    selector = SELECTORS.get(
                        name=key,
                        house=self.house,
                        origin=self.origin,
                        type="event",
                    )

                    event[key] = row.css(selector).get() if selector else ""

                event = self.preprocessor.fix(
                    event=event,
                    house=self.house,
                    origin=self.origin,
                )

                yield event
