import logging
from datetime import datetime


def format_date(date_str, date_str_format: str = '%d/%m/%Y', new_format: str = None) -> str:
    try:
        date_obj = datetime.strptime(date_str, date_str_format)
        if new_format:
            return date_obj.strftime(new_format)
        return date_obj.strftime(date_str_format)
    except Exception as e:
        logging.error(f"Formato de data invalido. Data {date_str}, formato esperado: {date_str_format}", e)
        return ''
