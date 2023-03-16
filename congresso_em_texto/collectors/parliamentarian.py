from scrapy import Spider


class ParliamentarianCollector(Spider):
    name = "parliamentarian-collector"

    def __init__(self, *args, **kwargs):
        super(ParliamentarianCollector, self).__init__(*args, **kwargs)

        self.model = {
            "id_parlamentar": None,
            "nome": None,
            "uf": None,
            "cargo": None,
            "legislatura": None,
            "partido": None,
        }

    def start_requests(self):
        pass

    def parse(self, response):
        pass
