import calendar
from datetime import datetime
from typing import Union

from sqlalchemy import func
from sqlalchemy.orm import Session

from json_generator_disp.helpers.logger import logger
from json_generator_disp.models import Bitacora as BitacoraModel

logging = logger()


class MonthLogs:
    """Monthyl logs for root JSON.."""
    def __init__(self, db_name: str, date: Union[datetime, str]):
        self.db_name = db_name
        self.date = date

    def build_month_logs(self, db: Session) -> dict:
        """Generate JSON of monthy logs."""
        dateTime = datetime.strptime(self.date, "%Y-%m-%d")
        year = dateTime.year
        month = dateTime.strftime('%m')
        day = dateTime.strftime('%d')
        last_day = calendar.monthrange(year, dateTime.month)[1]

        if logs := db.query(
            BitacoraModel.idBitacora.label("NumeroRegistro"),
            func.date_format(BitacoraModel.fechaYHoraEvento, "%Y-%m-%dT%H:%i:%s-06:00").label("FechaYHoraEvento"),
            BitacoraModel.usuario.label("UsuarioResponsable"),
            BitacoraModel.tipoEvento.label("TipoEvento"),
            BitacoraModel.descripcionEvento.label("DescripcionEvento")
            ).filter(
            BitacoraModel.fechaYHoraEvento.between(
                f"{year}-{month}-{day} 00:00:00",
                f"{year}-{month}-{last_day} 23:59:59",
            )).all():

            logs_list = [row._asdict() for row in logs]
            for log in logs_list:
                log["UsuarioResponsable"] = str(log["DescripcionEvento"]).split(
                    ": ")[1] if log["UsuarioResponsable"] == "" else log["UsuarioResponsable"]

                if log["TipoEvento"] in [20, 12, 7]:
                    event_type = {
                        "7": "sistemas de medicion",
                        "12": "sistemas de medicion",
                        "20": "sistemas de medicion",
                        }
                    log["IdentificacionComponenteAlarma"] = event_type[f'{log["TipoEvento"]}']

            return {"BitacoraMensual": logs_list}

        return {
            "BitacoraMensual": {
                "NumeroRegistro": 1,
                "FechaYHoraEvento": f"{year}-{month}-{day}T23:59:59-06:00",
                "UsuarioResponsable": self.db_name,
                "TipoEvento": 5,
                "DescripcionEvento": "Consulta de Informacion"
                }}

    def build_daily_logs(self, db: Session) -> dict:
        """Generate JSON of monthy logs."""
        date_time = datetime.strptime(self.date, "%Y-%m-%d")
        year = date_time.year
        month = date_time.strftime('%m')
        day = date_time.strftime('%d')

        if logs := db.query(
            BitacoraModel.idBitacora.label("NumeroRegistro"),
            func.date_format(BitacoraModel.fechaYHoraEvento, "%Y-%m-%dT%H:%i:%s-06:00").label("FechaYHoraEvento"),
            BitacoraModel.usuario.label("UsuarioResponsable"),
            BitacoraModel.tipoEvento.label("TipoEvento"),
            BitacoraModel.descripcionEvento.label("DescripcionEvento")
            ).filter(
            BitacoraModel.fechaYHoraEvento.between(
                f"{year}-{month}-{day} 00:00:00",
                f"{year}-{month}-{day} 23:59:59",
            )).all():

            logs_list = [row._asdict() for row in logs]
            for log in logs_list:
                log["UsuarioResponsable"] = str(log["DescripcionEvento"]).split(
                    ": ")[1] if log["UsuarioResponsable"] == "" else log["UsuarioResponsable"]

                if log["TipoEvento"] in [20, 12, 7]:
                    event_type = {
                        "7": "sistemas de medicion",
                        "12": "sistemas de medicion",
                        "20": "sistemas de medicion",
                        }
                    log["IdentificacionComponenteAlarma"] = event_type[f'{log["TipoEvento"]}']

            return {"Bitacora": logs_list}

        return {
            "Bitacora": {
                "NumeroRegistro": 1,
                "FechaYHoraEvento": f"{year}-{month}-{day}T23:59:59-06:00",
                "UsuarioResponsable": self.db_name,
                "TipoEvento": 5,
                "DescripcionEvento": "Consulta de Informacion"
                }}
