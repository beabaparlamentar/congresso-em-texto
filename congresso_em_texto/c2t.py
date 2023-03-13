import os
from datetime import datetime

import pandas as pd
from scrapy.crawler import CrawlerRunner
from twisted.internet import defer, reactor

from congresso_em_texto.collectors import EventCollector
from congresso_em_texto.collectors import ParliamentarianCollector
from congresso_em_texto.utils.constants import SETTINGS


class C2T:
    def __init__(self, start_date, end_date, house=None, origin=None):
        self.start_date = start_date
        self.end_date = end_date
        self.house = house
        self.origin = origin

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

    def run_parlamentarians_crawler(self):
        years = range(self.start_date.year - 3, self.end_date.year + 1)
        years = [year for year in years if ((year - 2) % 4 == 0)]

        collector = ParliamentarianCollector(years=years)
        collector.start_requests()

        for house in ["senate", "chamber"]:
            filepath = os.path.join("data", house, "parliamentarians")
            collector.save_data(house=house, filepath=filepath)

    def config_events_crawler(self, house, origin):
        directory = os.path.join("data", house, "events")
        filepath = os.path.join(directory, f"{house}-{origin}-events")

        dates = pd.date_range(
            start=datetime(self.start_date.year, 1, 1),
            end=datetime(self.end_date.year, 12, 31),
        ).tolist()

        self.crawlers.append(EventCollector)
        self.settings.append(SETTINGS.get_export_settings(filepath))
        self.parameters.append({"house": house, "origin": origin, "dates": dates})

    @defer.inlineCallbacks
    def setup_crawlers(self):
        for i, collector in enumerate(self.crawlers):
            process = CrawlerRunner(self.settings[i])
            yield process.crawl(collector, **self.parameters[i])
        reactor.stop()

    def run(self):
        # self.run_parlamentarians_crawler()

        # self.config_events_crawler(house="chamber", origin="plenary")
        self.config_events_crawler(house="chamber", origin="committee")
        self.setup_crawlers()
        reactor.run()
