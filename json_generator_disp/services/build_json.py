import json
from datetime import datetime
from typing import Union
from pprint import pprint
from sqlalchemy.orm import Session

from json_generator_disp.helpers.db import get_db
from json_generator_disp.models import Permiso

from .json_root import JsonRoot
from .product import ProductJson
from .month_logs import MonthLogs


class JsonBuilder:
    """Class for JSON building."""

    def __init__(self, db_name: str, date: Union[str, datetime]) -> None:
        self.db_name = db_name
        self.date = date

    def build_monthly_json(self) -> dict:
        """Month JSON."""
        print(">>>>>>>>>>>>>>MENSUAL", self.db_name, self.date, "<<<<<<<<<<<<<<")
        db = next(get_db(db_name=self.db_name))

        permiso = db.query(Permiso).limit(1).first()
        root_obj = JsonRoot(permiso=permiso, date=self.date)
        root_dict = root_obj.build_month_root()

        prod_obj = ProductJson(root=root_dict, date=self.date, db_name=self.db_name)
        prod_dict = prod_obj.build_monthly_product(db=db)
        # pprint(prod_dict)

        logs_obj = MonthLogs(db_name=self.db_name, date=self.date)
        logs_dict = logs_obj.build_month_logs(db=db)
        # pprint(logs_dict)

        root_dict.update(prod_dict)
        root_dict.update(logs_dict)

        json_name = root_obj.get_json_name()
        json_file = json.dumps(root_dict, ensure_ascii=False)
        json_file = json_file.encode("latin-1").decode("unicode_escape")

        return {
            "statusCode": 200,
            "body": {"json": json_file, "nombre": json_name},
        }

    def build_daily_json(self) -> dict:
        """daily JSON."""
        print(">>>>>>>>>>>>>>DIARIO", self.db_name, self.date, "<<<<<<<<<<<<<<")
        db = next(get_db(db_name=self.db_name))

        permiso = db.query(Permiso).limit(1).first()
        root_obj = JsonRoot(permiso=permiso, date=self.date)
        root_dict = root_obj.build_daily_root()
        # pprint(root_dict)

        prod_obj = ProductJson(root=root_dict, date=self.date, db_name=self.db_name)
        prod_dict = prod_obj.build_daily_product(db=db)
        # pprint(prod_dict)

        logs_obj = MonthLogs(db_name=self.db_name, date=self.date)
        logs_dict = logs_obj.build_daily_logs(db=db)
        # pprint(logs_dict)

        root_dict.update(prod_dict)
        root_dict.update(logs_dict)
        # pprint(root_dict)

        # pprint(json_name)
        json_name = root_obj.get_json_name()
        json_file = json.dumps(root_dict, ensure_ascii=False)
        json_file = json_file.encode("latin-1").decode("unicode_escape")

        return {
            "statusCode": 200,
            "body": {"json": json_file, "nombre": json_name},
        }
