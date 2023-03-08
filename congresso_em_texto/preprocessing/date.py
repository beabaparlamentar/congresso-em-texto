from datetime import datetime


class DatePreprocessor:
    def fix_date_pattern(self, date):
        return datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
