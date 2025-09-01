from datetime import timedelta
from typing import List, Dict, Any
from json_generator_disp.models import MovimientoDispensario as MovimientoDispensarioModel
from json_generator_disp.models import MedidorDispensario as MedidorDispensarioModel
from json_generator_disp.models import Manguera as MangueraModel
from json_generator_disp.models import Tanque as TanqueModel
from json_generator_disp.models import Dispensario as DispensarioModel
from json_generator_disp.models import ExistenciaDTanque
from json_generator_disp.helpers.enumerators import ComplementTypeEnum
from json_generator_disp.services.complement_factory import ComplementFactory


class Dispensary:
    """DispensarioModel data."""
    def __init__(
            self, subprod_key: int, disp: DispensarioModel,
            movements: List[MovimientoDispensarioModel],
            medidores: List[MedidorDispensarioModel],
            mangueras: List[MangueraModel]):
        """:param subproduct_key: claveSubProducto value.
        :param disp: ddbb DispensarioModel obj.
        :param movements: ddbb MovimientoDispensarioModel obj where movimiento attr == "Entrega".
        :param medidores: ddbb MedidorDispensarioModel list objs.
        :param mangueras: ddbb MangueraModel list objs."""
        self.subprod_key = subprod_key
        self.dispensary = disp
        self.disp_movements = movements
        self.disp_medidores = medidores
        self.disp_mangueras = mangueras

    def build_dispensary_data(self) -> Dict[str, Any]:
        """Build Dict with data of Dispensario.
        :return: Dictionary with movements data of the given dispensary."""
        print(f"{'':*^10} DISPENSARIO {'':*^10}")

        disp_data = {}

        disp_data["ClaveDispensario"] = self.dispensary.claveID
        disp_data["Medidores"] = []
        disp_data["Manguera"] = []

        disp_data.update({"Medidores": self._get_medidores_data()})
        disp_data.update({"Manguera": self._get_mangueras_data()})

        return disp_data

    def _get_medidores_data(self) -> List[Dict[str, Any]]:
        """Return dispensary deliveries."""
        disp_deliv_obj = DispDeliveries(medidores=self.disp_medidores)
        disp_deliv_data = disp_deliv_obj.build_medidores_data()

        return disp_deliv_data

    def _get_mangueras_data(self) -> List[Dict[str, Any]]:
        """Return list with mangueras data in."""
        disp_deliv_obj = DispDeliveries(deliveries=self.disp_movements, mangueras=self.disp_mangueras)
        disp_mang_list = disp_deliv_obj.build_mangueras_data()

        return disp_mang_list


class DispDeliveries:
    """Dispensary delivery data."""
    def __init__(self, deliveries: List[MovimientoDispensarioModel] = None,
                 medidores: List[MedidorDispensarioModel] = None,
                 mangueras: List[MangueraModel] = None):
        """:param subproduct_key: claveSubProducto value.
        :param disp: ddbb DispensarioModel obj.
        :param movements: ddbb MovimientoDispensarioModel obj where movimiento attr == "Entrega".
        :param medidores: ddbb MedidorDispensarioModel list objs.
        :param mangueras: ddbb MangueraModel list objs."""
        self.medidores = medidores
        self.deliveries = deliveries
        self.mangueras = mangueras

    def build_mangueras_data(self) -> List[Dict]:
        """Build list with data of mangueras.
        :return: List of dicts with data of the mangueras."""
        print(f"{'':*^10} MANGUERA {'':*^10}")
        manguera_list = []
        for mang in self.mangueras:
            manguera_data = {}
            mang_deliveries = [deliv for deliv in self.deliveries if deliv.claveIDispensario == mang.dispensario.claveID]

            manguera_data = {
                "IdentificadorManguera": mang.claveIM,
                "Entregas": self._build_mangueras_deliv_data(deliveries=mang_deliveries)
                }
            manguera_list.append(manguera_data)

        return manguera_list

    def build_medidores_data(self) -> List[Dict]:
        """Build data with medidores data in.
        :return: List of dicts with data of the medidores."""
        medidores_data = []

        for med in self.medidores:
            medidor_data = {}
            medidor_data["SistemaMedicionDispensario"] = med.sistemaMT
            medidor_data["LocalizODescripSistMedicionDispensario"] = med.localizODSMT
            medidor_data["VigenciaCalibracionSistMedicionDispensario"] = med.vigenciaCSMT.strftime("%Y-%m-%d")
            medidor_data["IncertidumbreMedicionSistMedicionDispensario"] = med.incertidumbreMSMT

            medidores_data.append(medidor_data)
        return medidores_data

    def _build_mangueras_deliv_data(self, deliveries: List[MovimientoDispensarioModel]) -> List[Dict[str, Any]]:
        """Build detailed list of deliveries data from manguera.
        :param deliveries: list of movimientos in dispensary.
        :return: List of dicts with delivery."""
        manguera_deliv_data = []

        for deliv in deliveries:
            deliv_detail_data = {}
            deliv_detail_data["NumeroDeRegistro"] = deliv.numeroDeRegistro or deliv.dispensario.idDispensario
            deliv_detail_data["TipoDeRegistro"] = deliv.tipoR
            deliv_detail_data["VolumenEntregadoTotalizadorAcum"] = round(deliv.volumenET, 3)
            deliv_detail_data["VolumenENtregadoTotalizadorInsta"] = round(deliv.volumenI, 3)
            # deliv_detail_data["PrecioVentaTotalizadorInsta"] =
            deliv_detail_data["FechaYHoraEntrega"] = deliv.fechaYHM.strftime("%Y-%m-%dT%H:%M:%S-06:00")
            # TODO COMPLEMENTO DE LAS ENTREGAS POR MANGUERA
            # deliv_detail_data["Complemento"] =
            manguera_deliv_data.append(deliv_detail_data)

        return {
            "TotalEntregas": len(deliveries),
            "SumaVolumenEntregado": round(sum(deliv.volumenI for deliv in deliveries), 3),
            "Entrega": manguera_deliv_data
            # TODO: COMPLEMENTOP
            # "TotalDocumentos": complemento_value
        }
