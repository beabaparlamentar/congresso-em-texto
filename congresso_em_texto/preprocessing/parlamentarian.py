from congresso_em_texto.preprocessing.date import DatePreprocessor
from congresso_em_texto.preprocessing.text import TextPreprocessor


class ParlamentarianPreprocessor(DatePreprocessor, TextPreprocessor):
    def fix(self, data):
        data = self.filter_elected_candidates(data)
        data = self.filter_parlamentarians(data)
        data = self.filter_columns(data)
        data = self.fix_values(data)

        return data

    def filter_elected_candidates(self, data):
        values = ["ELEITO", "ELEITO POR QP", "MÉDIA", "SUPLENTE", "ELEITO POR MÉDIA"]
        indexes = data["DS_SIT_TOT_TURNO"].isin(values)

        return data[indexes]

    def filter_parlamentarians(self, data):
        values = ["DEPUTADO FEDERAL", "SENADOR"]
        indexes = data["DS_CARGO"].isin(values)

        return data[indexes]

    def filter_columns(self, data):
        columns = {
            "id_parlamentar": "NR_CPF_CANDIDATO",
            "ano": "ANO_ELEICAO",
            "uf": "SG_UF",
            "cargo": "DS_CARGO",
            "nome": "NM_CANDIDATO",
            "nome_urna": "NM_URNA_CANDIDATO",
            "sigla_partido": "SG_PARTIDO",
            "partido": "NM_PARTIDO",
            "reeleicao": "ST_REELEICAO",
        }

        data = data[columns.values()]
        data.columns = columns.keys()

        return data

    def fix_values(self, data):
        data["reeleicao"] = data["reeleicao"] == "S"
        data["nome"] = data["nome"].apply(self.fix_proper_noun)
        data["partido"] = data["partido"].apply(self.fix_proper_noun)
        data["cargo"] = data["cargo"].apply(
            lambda c: "Senador(a)" if c == "SENADOR" else "Deputado(a) Federal"
        )

        data = data.drop_duplicates(subset=["ano", "id_parlamentar"])

        return data
