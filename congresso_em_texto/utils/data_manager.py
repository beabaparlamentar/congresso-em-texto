import os
import pandas as pd


class DataManager:
    """
    Classe responsável por verificar e ajustar a consistência dos dados coletados.
    """
    def __init__(self):
        """
        Inicializa o GerenciadorDados.
        """
        pass

    def verify_parliamentarians(self):
        """
        Verifica e ajusta a consistência dos dados sobre parlamentares coletados.
        """
        datasets_metadata = [
            {"house": "chamber", "filename": "deputies.csv"},
            {"house": "senate", "filename": "senators.csv"},
        ]

        for metadata in datasets_metadata:
            filepath = os.path.join("data", metadata.get("house"), "parliamentarians")
            filepath = os.path.join(filepath, metadata.get("filename"))

            if os.path.exists(filepath):
                data = pd.read_csv(filepath)
                data = data.query("id_parlamentar != 'id_parlamentar'")

                data = data.drop_duplicates(subset=["ano", "id_parlamentar"])
                data = data.sort_values(by=["ano", "id_parlamentar"])

                data.to_csv(filepath, index=False)

    def verify_events(self):
        """
        Verifica e ajusta a consistência dos dados sobre eventos coletados.
        """
        datasets_metadata = [
            {"house": "chamber", "filename": "chamber-committee-events.csv"},
            {"house": "chamber", "filename": "chamber-plenary-events.csv"},
        ]

        for metadata in datasets_metadata:
            filepath = os.path.join("data", metadata.get("house"), "events")
            filepath = os.path.join(filepath, metadata.get("filename"))

            if os.path.exists(filepath):
                data = pd.read_csv(filepath)
                data = data.query("id_evento != 'id_evento'")

                data = data.drop_duplicates(subset=["discursos"])
                data = data.dropna(subset=["data", "id_evento", "discursos"])
                data = data.sort_values(by=["data", "id_evento", "discursos"])

                data.to_csv(filepath, index=False)

    def verify_speeches(self):
        """
        Verifica e ajusta a consistência dos dados sobre discursos coletados.
        """
        datasets_metadata = [{"house": "chamber"}]

        for metadata in datasets_metadata:
            speeches_path = os.path.join("data", metadata.get("house"), "speeches")
            for path, _, filenames in os.walk(speeches_path):
                for filename in filenames:
                    filepath = os.path.join(path, filename)
                    data = pd.read_csv(filepath)
                    data = data.query("id_evento != 'id_evento'")

                    data = data.drop_duplicates(subset=["orador", "texto"])
                    data = data.dropna(subset=["orador", "texto"])
                    data = data.sort_values(by=["ordem_discurso"])
                    data["ordem_discurso"] = data.reset_index().index + 1

                    data.to_csv(filepath, index=False)

    def verify(self):
        """
        Executa a verificação dos dados coletados e ajusta a consistência quando necessário.
        """
        print("Iniciando verificação dos dados...")

        self.verify_parliamentarians()
        self.verify_events()
        self.verify_speeches()

        print("Verificação dos dados concluída!")
