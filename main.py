from datetime import datetime

from congresso_em_texto import C2T


if __name__ == "__main__":
    start_date = datetime.strptime("01/01/2003", "%d/%m/%Y")
    end_date = datetime.strptime("31/12/2022", "%d/%m/%Y")

    c2t = C2T(start_date=start_date, end_date=end_date)

    c2t.run()
