from datetime import datetime


date_format = ["%d/%m/%Y %H:%M:%S %z", "%d/%m/%Y %H:%M:%S %z %Z", "%d/%m/%Y %H:%M:%S", "%a, %d %b %Y %H:%M:%S %z",
               "%a, %d %b %Y %H:%M:%S %z %Z"]


def get_date(date: str) -> datetime:
    for f in date_format:
        try:
            return datetime.strptime(date, f)
        except Exception as e:
            # print("Err : " + str(e))
            continue
    return datetime.now()