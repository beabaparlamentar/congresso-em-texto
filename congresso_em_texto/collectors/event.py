from scrapy import Spider, FormRequest

from congresso_em_texto.preprocessing import EventPreprocessor
from congresso_em_texto.utils.constants import SELECTORS, URLS


class EventCollector(Spider):
    name = "event-collector"

    def __init__(self, house, origin, dates, *args, **kwargs):
        super(EventCollector, self).__init__(*args, **kwargs)

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
        if self.house == "senate":
            pass
        if self.house == "chamber":
            return self.start_chamber_requests()

    def start_chamber_requests(self):
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
