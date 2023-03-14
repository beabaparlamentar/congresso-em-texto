from dataclasses import dataclass


@dataclass(frozen=True)
class SettingsNamespace:
    DEFAULT = {
        "USER_AGENT": "Congresso em Texto",
        "LOG_LEVEL": "ERROR",
        "DNS_TIMEOUT": 180,
        "AUTOTHROTTLE_ENABLED": True,
        "COOKIES_ENABLED": False,
        "ROBOTSTXT_OBEY": True,
    }

    def get_default_settings(self):
        return self.DEFAULT.copy()

    def get_export_settings(self, filepath):
        settings = self.get_default_settings()
        settings["FEEDS"] = {f"{filepath}.csv": {"format": "csv", "encoding": "utf-8"}}

        return settings


SETTINGS = SettingsNamespace()
