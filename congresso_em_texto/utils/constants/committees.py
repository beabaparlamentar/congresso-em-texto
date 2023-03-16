from dataclasses import dataclass


@dataclass(frozen=True)
class CommitteesNamespace:
    CHAMBER = {
        "CAPADR": (
            "Comissão de Agricultura, Pecuária, Abastecimento e Desenvolvimento Rural"
        ),
        "CC": "Comissão de Cultura",
        "CCJC": "Comissão de Constituição e Justiça e de Cidadania",
        "CCTCI": "Comissão de Ciência e Tecnologia, Comunicação e Informática",
        "CDC": "Comissão de Defesa do Consumidor",
        "CDDM": "Comissão de Defesa dos Direitos da Mulher",
        "CDDPD": "Comissão de Defesa dos Direitos das Pessoas com Deficiência",
        "CDDPI": "Comissão de Defesa dos Direitos da Pessoa Idosa",
        "CDEICS": (
            "Comissão de Desenvolvimento Econômico, Indústria, Comércio e Serviços"
        ),
        "CDHM": "Comissão de Direitos Humanos e Minorias",
        "CDU": "Comissão de Desenvolvimento Urbano",
        "CEdu": "Comissão de Educação",
        "CEsp": "Comissão do Esporte",
        "CFFC": "Comissão de Fiscalização Financeira e Controle",
        "CFT": "Comissão de Finanças e Tributação",
        "CINDRA": (
            "Comissão de Integração Nacional, Desenvolvimento Regional e Amazônia"
        ),
        "CLP": "Comissão de Legislação Participativa",
        "CMADS": "Comissão de Meio Ambiente e Desenvolvimento Sustentável",
        "CME": "Comissão de Minas e Energia",
        "CREDN": "Comissão de Relações Exteriores e de Defesa Nacional",
        "CSPCCO": "Comissão de Segurança Pública e Combate ao Crime Organizado",
        "CSSF": "Comissão de Seguridade Social e Família",
        "CT": "Comissão de Turismo",
        "CTASP": "Comissão de Trabalho, de Administração e Serviço Público",
        "CVT": "Comissão de Viação e Transportes",
    }

    def get(self, acronym, house):
        if house == "chamber":
            return self.CHAMBER.get(acronym, "")

        return ""

    def to_list(self, house):
        if house == "chamber":
            return self.CHAMBER.values()

        return []


COMMITTEES = CommitteesNamespace()
