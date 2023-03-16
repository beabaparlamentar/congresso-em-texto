import os
from datetime import datetime

import pandas as pd
from scrapy.crawler import CrawlerRunner
from twisted.internet import defer, reactor

from congresso_em_texto.collectors import EventCollector
from congresso_em_texto.utils.constants import SETTINGS


class C2T:
    def __init__(self, start_date, end_date, house=None, origin=None):
        self.start_date = start_date
        self.end_date = end_date
        self.house = house
        self.origin = origin

        self.collectors = []
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

    def config_chamber_committee_events(self):
        directory = os.path.join("data", "chamber", "events")
        filepath = os.path.join(directory, "chamber-committee-events")

        dates = pd.date_range(
            start=datetime(self.start_date.year, 1, 1),
            end=datetime(self.end_date.year, 12, 31),
        ).tolist()

        self.collectors.append(EventCollector)
        self.settings.append(SETTINGS.get_export_settings(filepath))
        self.parameters.append(
            {"house": "chamber", "origin": "committee", "dates": dates}
        )

    def config_chamber_plenary_events(self):
        directory = os.path.join("data", "chamber", "events")
        filepath = os.path.join(directory, "chamber-plenary-events")

        dates = pd.date_range(
            start=datetime(self.start_date.year, 1, 1),
            end=datetime(self.end_date.year, 12, 31),
        ).tolist()

        self.collectors.append(EventCollector)
        self.settings.append(SETTINGS.get_export_settings(filepath))
        self.parameters.append(
            {"house": "chamber", "origin": "plenary", "dates": dates}
        )

    @defer.inlineCallbacks
    def setup_crawlers(self):
        for i, collector in enumerate(self.collectors):
            process = CrawlerRunner(self.settings[i])
            yield process.crawl(collector, **self.parameters[i])
        reactor.stop()

    def run(self):
        self.config_chamber_plenary_events()
        self.config_chamber_committee_events()

        self.setup_crawlers()
        reactor.run()
