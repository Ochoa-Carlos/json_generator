from datetime import datetime
import uuid
from typing import Union
from json_generator_disp.helpers.constants import VERSION
from json_generator_disp.models import Permiso
from json_generator_disp.helpers.enumerators import CaracterEnum
from json_generator_disp.helpers.logger import logger


logging = logger()

class JsonRoot:
    """Root class for JSON."""

    def __init__(self, permiso: Permiso, date: Union[datetime, str]):
        self.permiso = permiso
        self.date = date
        self.json_type = None
        self.periodo = None

    def build_month_root(self) -> dict:
        """Return montly JSON root builded."""
        try:
            date = datetime.strptime(self.date, "%Y-%m-%d")
            year = date.year
            month = date.strftime('%m')
            day = date.strftime('%d')
            self.json_type = "M"
            self.periodo = f"{year}-{month}-{day}"

            root = {
                "Version": VERSION,
                "RfcContribuyente": None,
                "RfcRepresentanteLegal": None,
                "RfcProveedor": None,
                # VER CUANDO SI APLICA
                # "RfcProveedores": None,
                "Caracter": None,
                "ModalidadPermiso": None,
                "NumPermiso": None,
                "NumContratoOAsignacion": None,
                "InstalacionAlmacenGasNatural": None,
                "ClaveInstalacion": None,
                "DescripcionInstalacion": None,
                # VER CUANDO SI APLICA
                # "Geolocalizacion": [],
                "NumeroPozos": 0,
                "NumeroTanques": 0,
                "NumeroDuctosEntradaSalida": 0,
                "NumeroDuctosTransporteDistribucion": 0,
                "NumeroDispensarios": 0,
                "Producto": [],
                "BitacoraMensual": {}
            }

            root.update(self._set_permiso_data())
            root.update(self._set_caracter_data())
            root.update(self._set_report_date())
            self._validate_fields(root=root)

            for key in list(root.keys()):
                # if root[key] is None:
                if root.get(key) is None:
                    root.pop(key)

            return root
        except Exception as exc:
            logging.error(f"Error raiz: {exc}")
            return {}

    def build_daily_root(self) -> dict:
        """Return daily JSON root builded."""
        try:
            date = datetime.strptime(self.date, "%Y-%m-%d")
            year = date.year
            month = date.strftime('%m')
            day = date.strftime('%d')
            self.json_type = "D"
            self.periodo = f"{year}-{month}-{day}"

            root = {
                "Version": VERSION,
                "RfcContribuyente": None,
                "RfcRepresentanteLegal": None,
                "RfcProveedor": None,
                # VER CUANDO SI APLICA
                # "RfcProveedores": None,
                "Caracter": None,
                "ModalidadPermiso": None,
                "NumPermiso": None,
                "NumContratoOAsignacion": None,
                "InstalacionAlmacenGasNatural": None,
                "ClaveInstalacion": None,
                "DescripcionInstalacion": None,
                # VER CUANDO SI APLICA
                # "Geolocalizacion": [],
                "NumeroPozos": 0,
                "NumeroTanques": 0,
                "NumeroDuctosEntradaSalida": 0,
                "NumeroDuctosTransporteDistribucion": 0,
                "NumeroDispensarios": 0,
                "FechaYHoraCorte": None,
                "Producto": [],
                "Bitacora": {}
            }

            root.update(self._set_permiso_data())
            root.update(self._set_caracter_data())
            root.update(self._set_report_date())
            self._validate_fields(root=root)

            for key in list(root.keys()):
                # if root[key] is None:
                if root.get(key) is None:
                    root.pop(key)

            return root
        except Exception as exc:
            logging.error(f"Error raiz: {exc}")
            return {}

    def get_json_name(self) -> str:
        """Get json filename."""
        try:
            tipo = self.json_type
            myuuid = uuid.uuid4()
            rfc_cv = self.permiso.rfcContribuyente
            rfv_pr = self.permiso.rfcProveedor
            periodo = self.periodo
            inst_key = self.permiso.claveInstalacion
            report_type = self.permiso.claveInstalacion[0][:3]
            t_standard = "JSON"
            json_name = f"{tipo}_{myuuid}_{rfc_cv}_{rfv_pr}_{periodo}_{inst_key}_{report_type}_{t_standard}"
            return json_name
        except Exception as exc:
            logging.error(f"Error: {exc}")
            return ""

    def _set_permiso_data(self) -> dict:
        return {
            "RfcContribuyente": self.permiso.rfcContribuyente,
            "RfcRepresentanteLegal": self.permiso.rfcRepresentanteLegal,
            "RfcProveedor": self.permiso.rfcProveedor,
            "ClaveInstalacion": self.permiso.claveInstalacion,
            "DescripcionInstalacion": self.permiso.descripcionInstalacion,
            # "Geolocalizacion": [{
            #     "GeolocalizacionLatitud": self.permiso.latitud,
            #     "GeolocalizacionLongitud": self.permiso.longitud
            #     }],
            "NumeroPozos": self.permiso.nPozos or 0,
            "NumeroTanques": self.permiso.nTanques or 0,
            "NumeroDuctosEntradaSalida": self.permiso.nDuctosEntradaSalida or 0,
            "NumeroDuctosTransporteDistribucion": self.permiso.nDuctosTransporteDistribucion or 0,
            "NumeroDispensarios":self.permiso.nDispensarios or 0
        }

    def _set_caracter_data(self) -> dict:
        caracter_keys = CaracterEnum[self.permiso.caracter.upper()].value
        return {** {key[0].upper() + key[1:]: getattr(self.permiso, key) for key in caracter_keys},
                "Caracter": self.permiso.caracter}

    def _set_report_date(self) -> dict:
        return {
            "FechaYHoraCorte": datetime.strftime(
                datetime.strptime(self.date, "%Y-%m-%d"), "%Y-%m-%d")+"T23:59:59-06:00"
        }

    # TODO validar diccionario durante la creacion
    def _validate_fields(self, root: dict) -> None:
        ...
