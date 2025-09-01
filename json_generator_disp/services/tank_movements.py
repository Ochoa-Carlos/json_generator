from datetime import timedelta
from typing import List, Dict, Any
from json_generator_disp.models import MovimientoTanque as MovimientoTanqueModel
from json_generator_disp.models import Tanque as TanqueModel
from json_generator_disp.models import ExistenciaDTanque
from json_generator_disp.models import ExistenciaDTanque as ExistenciaDTanqueModel
from json_generator_disp.helpers.enumerators import ComplementTypeEnum, ProductKeyEnum
from json_generator_disp.services.complement_factory import ComplementFactory

class Tank:
    """TanqueModel data"""
    def __init__(self, tank: TanqueModel,
                 movements: List[MovimientoTanqueModel], existances: ExistenciaDTanqueModel):
        """:param tank: ddbb TanqueModel obj.
        :param movements: ddbb MovimientoTanqueModel obj where movimiento attr in ["Recepcion", "Entrega"]
        :param existances: ddbb ExistenciaDTanqueModel obj."""
        self.tank = tank
        self.tank_movements = movements
        self.tank_existances = existances

    def build_tank_data(self) -> Dict[str, Any]:
        """Build Dict with data of Tanque.
        :return: Dictionary with movements data of the given tank."""
        tank_data = {}

        tank_data["ClaveIdentificacionTanque"] = self.tank.clave
        tank_data["Localizaciony/oDescripcionTanque"] = self.tank.locDesTanque
        tank_data["VigenciaCalibracionTanque"] = self.tank.vigenciaCT.strftime("%Y-%m-%d")
        tank_data["CapacidadTotalTanque"] = self.tank.capacidadTT
        tank_data["CapacidadOperativaTanque"] = self.tank.capacidadOT
        tank_data["CapacidadUtilTanque"] = self.tank.capacidadTT - self.tank.volumenMO
        tank_data["CapacidadFondajeTanque"] = self.tank.capacidadFT
        if self.tank.producto.claveProducto == ProductKeyEnum.PR09.value:
            tank_data["CapacidadGasTalon"] = self.tank.capacidadGT
        tank_data["VolumenMinimoOperacion"] = self.tank.volumenMO
        tank_data["EstadoTanque"] = self.tank.estadoTanque
        tank_data["Medidores"] = [{
            "SistemaMedicionTanque": self.tank.medidor_tanque[0].sistemaMT,
            "LocalizODescripSistMedicionTanque": self.tank.medidor_tanque[0].localizODSMT,
            "VigenciaCalibracionSistMedicionTanque": self.tank.medidor_tanque[0].VigenciaCSMT.strftime("%Y-%m-%d"),
            "IncertidumbreMedicionSistMedicionTanque": self.tank.medidor_tanque[0].incertidumbreMSMT,
            }]

        tank_data.update({"Recepciones": self._get_tank_receptions(tank=self.tank, movements=self.tank_movements)})
        tank_data.update({"Entregas": self._get_tank_deliveries(tank=self.tank, movements=self.tank_movements)})
        tank_data.update({"Existencias": self._get_tank_existances(existances=self.tank_existances)})

        return tank_data

    def _get_tank_receptions(self, tank: TanqueModel, movements: List[MovimientoTanqueModel]) -> List[Dict]:
        """Return tank receptions ."""
        recept_movs = [mov for mov in movements if mov.movimiento == "Recepcion"]

        recepciones_obj = TankReceptions(tank=tank, receptions=recept_movs) 
        receptions_dict = recepciones_obj.build_tank_receptions()

        return [receptions_dict]

    def _get_tank_deliveries(self, tank: TanqueModel, movements: List[MovimientoTanqueModel]) -> List:
        """Return tank deliveries."""
        deliv_movs = [mov for mov in movements if mov.movimiento == "Entrega"]

        deliveries_obj = TankDeliveries(tank=tank, deliveries=deliv_movs)
        deliveries_dict = deliveries_obj.build_tank_deliveries()

        return [deliveries_dict]

    def _get_tank_existances(self, existances: List[ExistenciaDTanqueModel]) -> List:
        """Return existances"""
        exist_obj = Existances(existances=existances)
        existances_dict = exist_obj.build_tank_existances()

        return existances_dict


class TankReceptions:
    """Receptions movements in Tank."""
    def __init__(self, tank: TanqueModel, receptions: List[MovimientoTanqueModel]):
        """:param tank: ddbb TanqueModel obj.
        :param receptions: ddbb MovimientoTanqueModel obj where movimiento attr == "Recepcion".."""
        self.tank = tank
        self.receptions = receptions
        self._receptions_list = []

    def build_tank_receptions(self) -> Dict[str, Any]:
        """Build Dict with receptions in the given Tank.
        :return: Dictionary with receptions data."""
        recepts_data = {}

        recepts_data["TotalRecepciones"] = len(self.receptions)
        recepts_data["SumaVolumenRecepcion"] = {
            "ValorNumerico": sum(
                mov.volumenMovimiento for mov in self.receptions
                ),
            "UnidadDeMedida": self.tank.producto.unidadMedida
            }
        recepts_data["TotalDocumentos"] = len(
            {mov.cfdi for mov in self.receptions if mov.cfdi}
            )
        recepts_data["SumaCompras"] = sum(
            (mov.cfdi_rel.contraprestacion if mov.cfdi_rel else 0)
            for mov in {mov.cfdi: mov for mov in self.receptions}.values()
            )

        if recepts_data.get("TotalRecepciones") > 0:
            self._build_detailed_reception()

        if len(self._receptions_list) > 0:
            recepts_data["Recepcion"] = self._receptions_list

        return recepts_data

    def _build_detailed_reception(self) -> None:
        """Append receptions information to the instance list.
        :return: None."""
        for reception in self.receptions:
            recept_data = {}

            recept_data["NumeroDeRegistro"] = reception.idMovimiento
            recept_data["VolumenInicialTanque"] = {
                "ValorNumerico": round(reception.volumenIT, 3),
                "UnidadMedida": reception.producto.unidadMedida
            }
            recept_data["VolumenFinalTanque"] = reception.volumenFT
            recept_data["VolumenRecepcion"] = {
                "ValorNumerico": round(reception.volumenMovimiento, 3),
                "UnidadMedida": reception.producto.unidadMedida
            }
            recept_data["Temperatura"] = reception.temperatura
            recept_data["PresionAbsoluta"] = reception.presionAbsoluta
            recept_data["FechaYHoraInicioRecepcion"] = reception.fechaYHIM.strftime("%Y-%m-%dT%H:%M:%S%z-06:00")
            recept_data["FechaYHoraFinalRecepcion"] = reception.fechaYHFM.strftime("%Y-%m-%dT%H:%M:%S%z-06:00")

            if reception.cfdi:
                recep_cfdi = [reception.cfdi_rel]
                complement = ComplementTypeEnum.ALMACENAMIENTO.value
                reception_complement = ComplementFactory.build_month_complement(
                    complement=complement, cfdis=recep_cfdi
                    )
                recept_data["Complemento"] = reception_complement.get("Complemento")

            self._receptions_list.append(recept_data)


class TankDeliveries:
    """Deliveries from tank"""
    def __init__(self, tank: TanqueModel, deliveries: List[MovimientoTanqueModel]):
        """:param tank: ddbb TanqueModel obj.
        :param deliveries: ddbb MovimientoTanqueModel obj where movimiento attr == "Entrega"."""
        self.tank = tank
        self.deliveries = deliveries
        self._deliveries_list = []

    def build_tank_deliveries(self) -> Dict[str, Any]:
        """Build Dict with deliveries in the given Tank.
        :return: Dictionary with deliveries data."""
        delivs_data = {}

        delivs_data["TotalEntregas"] = sum(
            1 for _ in self.deliveries
            )
        delivs_data["SumaVolumenEntregado"] = {
            "ValorNumerico": sum(
                mov.volumenMovimiento for mov in self.deliveries
                ),
            "UnidadDeMedida": self.tank.producto.unidadMedida
            }
        delivs_data["TotalDocumentos"] = len(
            {mov.cfdi for mov in self.deliveries if mov.cfdi}
            )
        delivs_data["SumaVentas"] = sum(
            (mov.cfdi_rel.contraprestacion if mov.cfdi_rel else 0)
            for mov in {mov.cfdi: mov for mov in self.deliveries}.values()
            )

        if delivs_data.get("TotalEntregas") > 0:
            self._build_detailed_delivery()
        if len(self._deliveries_list) > 0:
            delivs_data["Entregas"] = self._deliveries_list

        return delivs_data

    def _build_detailed_delivery(self) -> None:
        """Append deliveries information to the instance list.
        :return: None."""
        for delivery in self.deliveries:
            deliv_data = {}

            deliv_data["NumeroDeRegistro"] = delivery.idMovimiento
            deliv_data["VolumenInicialTanque"] = {
                "ValorNumerico": round(delivery.volumenIT, 3),
                "UnidadMedida": delivery.producto.unidadMedida
                }
            deliv_data["VolumenFinalTanque"] = delivery.volumenFT
            deliv_data["VolumenEntregado"] = {
                "ValorNumerico": round(delivery.volumenMovimiento, 3),
                "UnidadMedida": delivery.producto.unidadMedida
            }
            deliv_data["Temperatura"] = delivery.temperatura
            deliv_data["PresionAbsoluta"] = delivery.presionAbsoluta
            deliv_data["FechaYHoraInicialEntrega"] = delivery.fechaYHIM.strftime("%Y-%m-%dT%H:%M:%S%z-06:00")
            deliv_data["FechaYHoraFinalEntrega"] = delivery.fechaYHIM.strftime("%Y-%m-%dT%H:%M:%S%z-06:00")

            if delivery.cfdi:
                recep_cfdi = [delivery.cfdi_rel]
                complement = ComplementTypeEnum.ALMACENAMIENTO.value
                reception_complement = ComplementFactory().build_month_complement(
                    complement=complement, cfdis=recep_cfdi
                    )
                deliv_data["Complemento"] = reception_complement.get("Complemento")

            self._deliveries_list.append(deliv_data)


# TODO existances could being calculated using Tanque records, try to include it if not existances records.
class Existances:
    """Daily existances """
    def __init__(self, existances: List[ExistenciaDTanque]):
        self.existances = existances
        self.existances_list = []

    def build_tank_existances(self) -> Dict[str, Any]:
        """Build obj of existances."""
        exist_data = {}

        yhem_date = self.existances.fechaYHEM.strftime("%Y-%m-%dT23:59:59-06:00")
        yham_date = (self.existances.fechaYHEM + timedelta(days=-1)).strftime("%Y-%m-%dT23:59:59-06:00")

        exist_data["VolumenExistenciasAnterior"] = self.existances.volumenEA
        exist_data["VolumenAcumOpsRecepcion"] = self.existances.volumenAOR
        exist_data["HoraRecepcionAcumulado"] = "23:59:59-06:00"
        exist_data["VolumenAcumOpsEntrega"] = self.existances.volumenEA
        exist_data["HoraEntregaAcumulado"] = "23:59:59-06:00"
        exist_data["VolumenExistencias"] = self.existances.volumenExistencias
        exist_data["FechaYHoraEstaMedicion"] = yhem_date
        exist_data["FechaYHoraMedicionAnterior"] = yham_date

        return exist_data
