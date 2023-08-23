from datetime import datetime


class DatePreprocessor:
    """
    Classe para pré-processamento de datas.
    """
    def fix_date_pattern(self, date):
        """
        Converte uma data de um padrão para outro.

        Args:
            date (str): A data no formato "%d/%m/%Y".

        Returns:
            str: A data convertida no formato "%Y-%m-%d".
        """
        return datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
