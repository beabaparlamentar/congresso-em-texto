from congresso_em_texto.preprocessing.text import TextPreprocessor


class ParliamentarianPreprocessor(TextPreprocessor):
    """
    Classe para pré-processamento de informações parlamentares.
    """
    def fix(self, data):
        """
        Aplica correções e pré-processamento aos dados dos parlamentares.

        Args:
            data (DataFrame): Dados dos parlamentares.

        Returns:
            DataFrame: Dados dos parlamentares após correções e pré-processamento.
        """
        data = self.filter_elected_candidates(data)
        data = self.filter_parliamentarians(data)
        data = self.filter_columns(data)
        data = self.fix_values(data)

        return data

    def filter_elected_candidates(self, data):
        """
        Filtra os dados para manter somente candidatos eleitos.

        Args:
            data (DataFrame): Dados dos parlamentares.

        Returns:
            DataFrame: Dados filtrados mantendo apenas candidatos eleitos.
        """
        values = ["ELEITO", "ELEITO POR QP", "MÉDIA", "SUPLENTE", "ELEITO POR MÉDIA"]
        indexes = data["DS_SIT_TOT_TURNO"].isin(values)

        return data[indexes]

    def filter_parliamentarians(self, data):
        """
        Filtra os dados para manter somente parlamentares.

        Args:
            data (DataFrame): Dados dos parlamentares.

        Returns:
            DataFrame: Dados filtrados mantendo apenas parlamentares.
        """
        values = ["DEPUTADO FEDERAL", "SENADOR"]
        indexes = data["DS_CARGO"].isin(values)

        return data[indexes]

    def filter_columns(self, data):
        """
        Filtra as colunas relevantes nos dados.

        Args:
            data (DataFrame): Dados dos parlamentares.

        Returns:
            DataFrame: Dados mantendo apenas as colunas relevantes.
        """
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
        """
        Aplica correções específicas aos valores dos dados.

        Args:
            data (DataFrame): Dados dos parlamentares.

        Returns:
            DataFrame: Dados com valores corrigidos.
        """
        data["reeleicao"] = data["reeleicao"] == "S"
        data["nome"] = data["nome"].apply(self.fix_proper_noun)
        data["partido"] = data["partido"].apply(self.fix_proper_noun)
        data["cargo"] = data["cargo"].apply(
            lambda c: "Senador(a)" if c == "SENADOR" else "Deputado(a) Federal"
        )

        data = data.drop_duplicates(subset=["ano", "id_parlamentar"])

        return data
