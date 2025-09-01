import calendar
from datetime import datetime
from typing import Union

from sqlalchemy import func
from sqlalchemy.orm import Session

from json_generator_disp.helpers.logger import logger
from json_generator_disp.models import MovimientoTanque as MovimientoTanqueModel

logging = logger()


class ComplementBase:
    """Complement for product json."""
    def __init__(self, movements: MovimientoTanqueModel, db_name: str, date: Union[datetime, str]):
        self.movements = movements
        self.db_name = db_name
        self.date = date

    def build_month_complement(self) -> dict:
        """Build monthly complement."""
        print("===================== complemento=====================  ")
