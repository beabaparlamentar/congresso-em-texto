import os
from datetime import datetime

import pandas as pd
from scrapy.crawler import CrawlerRunner
from twisted.internet import defer, reactor

from congresso_em_texto.collectors import EventCollector
from congresso_em_texto.collectors import ParliamentarianCollector
from congresso_em_texto.collectors import SpeechCollector
from congresso_em_texto.utils.constants import SETTINGS


class C2T:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.crawlers = []
        self.settings = []
        self.parameters = []

        self.create_directories()

    def create_directories(self):
        years = range(self.start_date.year, self.end_date.year + 1)
        months = range(1, 13)

        paths = [
            os.path.join("data", "chamber", "events"),
            os.path.join("data", "senate", "events"),
            os.path.join("data", "chamber", "parliamentarians"),
            os.path.join("data", "senate", "parliamentarians"),
        ]

        for year in [f"{y}" for y in years]:
            for month in [f"{m:02d}" for m in months]:
                paths.append(os.path.join("data", "chamber", "speeches", year, month))
                paths.append(os.path.join("data", "senate", "speeches", year, month))

        for p in paths:
            if not os.path.exists(p):
                os.makedirs(p)

    def collect_parlamentarians(self):
        collector = ParliamentarianCollector(
            start_date=self.start_date,
            end_date=self.end_date,
        )

        collector.start_requests()
        houses = ["senate", "chamber"]

        for house in houses:
            filename = "senadores.csv" if house == "senate" else "deputados.csv"
            filepath = os.path.join("data", house, "parliamentarians", filename)
            collector.save_data(house=house, filepath=filepath)

    def config_events_crawler(self, house, origin):
        filename = f"{house}-{origin}-events"
        filepath = os.path.join("data", house, "events", filename)

        self.crawlers.append(EventCollector)
        self.settings.append(SETTINGS.get_export_settings(filepath))
        self.parameters.append(
            {
                "house": house,
                "origin": origin,
                "start_date": self.start_date,
                "end_date": self.end_date,
            }
        )

    def config_speeches_crawler(self, house, origin):
        filename = f"{house}-{origin}-events.csv"
        filepath = os.path.join("data", house, "events", filename)

        events = pd.read_csv(
            filepath,
            parse_dates=["data"],
            date_parser=lambda x: datetime.strptime(x, "%Y-%m-%d"),
        )

        events = events.query("@self.start_date <= data <= @self.end_date")
        speeches_path = os.path.join("data", house, "speeches")

        self.crawlers.append(SpeechCollector)
        self.settings.append(SETTINGS.get_default_settings())
        self.parameters.append(
            {
                "house": house,
                "origin": origin,
                "events": events,
                "directory": speeches_path,
            }
        )

    @defer.inlineCallbacks
    def setup_crawlers(self):
        for i, collector in enumerate(self.crawlers):
            process = CrawlerRunner(self.settings[i])
            yield process.crawl(collector, **self.parameters[i])
        reactor.stop()

    def run(self):
        self.collect_parlamentarians()

        self.config_events_crawler(house="chamber", origin="plenary")
        self.config_events_crawler(house="chamber", origin="committee")

        self.config_speeches_crawler(house="chamber", origin="plenary")
        self.config_speeches_crawler(house="chamber", origin="committee")

        self.setup_crawlers()
        reactor.run()
