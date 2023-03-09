from dataclasses import dataclass


@dataclass(frozen=True)
class UrlsNamespace:
    CANDIDATES = (
        "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_"
    )
    DOMAIN = {
        "chamber": "https://www.camara.leg.br",
        "senate": "https://www12.senado.leg.br",
    }
    SEARCH = {
        "chamber": (
            "https://www.camara.leg.br/internet/sitaqweb/resultadoPesquisaDiscursos.asp"
        )
    }
    SPEECH = {"chamber": "https://www.camara.leg.br/internet/sitaqweb/"}

    def get_candidates_url(self, year):
        return self.CANDIDATES + f"{year}.zip"

    def get_domain_url(self, house):
        return self.DOMAIN.get(house, "")

    def get_search_url(self, house):
        return self.SEARCH.get(house, "")

    def get_speech_url(self, house):
        return self.SPEECH.get(house, "")


URLS = UrlsNamespace()
