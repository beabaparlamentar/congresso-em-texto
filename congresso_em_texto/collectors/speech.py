from scrapy import Spider


class SpeechCollector(Spider):
    name = "speech-collector"

    def __init__(self, *args, **kwargs):
        super(SpeechCollector, self).__init__(*args, **kwargs)

        self.model = {
            "id_evento": None,
            "ordem_discurso": None,
            "orador": None,
            "texto": None,
        }

    def start_requests(self):
        pass

    def parse(self, response):
        pass
