import calendar
from datetime import datetime
from typing import Union, Optional, List


from json_generator_disp.helpers.constants import VERSION
from json_generator_disp.helpers.enumerators import CaracterEnum
from json_generator_disp.helpers.logger import logger
from json_generator_disp.models import MovimientoTanque as MovimientoTanqueModel
from json_generator_disp.models import MovimientoDispensario as MovimientoDispensarioModel
from json_generator_disp.models import Permiso
from json_generator_disp.models import Producto as ProductModel
from json_generator_disp.models import ExistenciaDTanque as ExistenciasDModel
from json_generator_disp.models import Cfdi as CfdiModel
from json_generator_disp.models import Dictamen as DictamenModel
from json_generator_disp.models import Certificado as CertificadoModel
from json_generator_disp.services.complement_factory import ComplementFactory
from json_generator_disp.helpers.enumerators import ComplementTypeEnum

logging = logger()

class VolumeMonthlyReportJson:
    """Volumetric Control Report Class."""

    def __init__(self, receptions: List[MovimientoTanqueModel], deliveries: List[MovimientoDispensarioModel],
                 dictamen: Optional[DictamenModel], product: ProductModel,
                 certificate: Optional[CertificadoModel],
                 existances: Optional[List[ExistenciasDModel]], cfdis: List[CfdiModel]):
        self.receptions = receptions
        self.deliveries = deliveries
        self.cfdis = cfdis
        self.existances = existances
        self.dictamen = dictamen
        self.certificate = certificate
        self.product = product
        self.date = None
        self.complement_factory = ComplementFactory

    def build_month_report(self, date: Union[datetime, str]) -> dict:
        """Generate JSON of monthy volume control."""
        self.date = date
        report_dict = {
            "ControlDeExistencias": None,
            "Recepciones": None,
            "Entregas": None
        }
        report_dict.update(self._set_control_existencias(date=date))
        report_dict.update(self._set_receptions())
        report_dict.update(self._set_deliveries())

        return report_dict

    def _set_control_existencias(self,date: Union[datetime, str]) -> dict:
        data = {}
        date_time = datetime.strptime(date, "%Y-%m-%d")
        year = date_time.year
        month = date_time.strftime('%m')
        last_day = calendar.monthrange(year, date_time.month)[1]

        data["VolumenExistenciasMes"] = self.existances[-1].volumenExistencias if self.existances else 0.0
        data["FechaYHoraEstaMedicionMes"] = f"{year}-{month}-{last_day}T23:59:59-06:00"

        return {"ControlDeExistencias": data}

    def _set_receptions(self) -> dict:
        data = {}

        data["TotalRecepcionesMes"] = len(self.receptions)
        data["SumaVolumenRecepcionMes"] = {
            "ValorNumerico": round(sum(rec.volumenMovimiento for rec in self.receptions), 2),
            "UnidadDeMedida": self.product.unidadMedida
            }

        if self.product.claveProducto == "PR09":
            data["PoderCalorifico"] = {
                "ValorNumerico": float(format(0, '.1f')),
                "UnidadDeMedida": self.product.unidadMedida
            }

        data.update(self._set_receptions_complement())
        data["TotalDocumentosMes"] = len(data["Complemento"])
        data["ImporteTotalRecepcionesMensual"] = round(sum({
            rec.cfdi: rec.cfdi_rel.contraprestacion
            for rec in self.receptions if rec.cfdi
            }.values()), 3)

        return {"Recepciones": data}

    def _set_deliveries(self) -> dict:
        data = {}

        data["TotalEntregasMes"] = len(self.deliveries)
        data["SumaVolumenEntregadoMes"] = {
            "ValorNumerico": round(sum(deliv.volumenI for deliv in self.deliveries), 2),
            "UnidadDeMedida": self.product.unidadMedida
        }

        if self.product.claveProducto == "PR09":
            data["PoderCalorifico"] = {
                "ValorNumerico": float(format(0, '.1f')),
                "UnidadDeMedida": self.product.unidadMedida
            }

        data.update(self._set_deliveries_complement())
        data["TotalDocumentosMes"] = len(data["Complemento"])
        data["ImporteTotalEntregasMes"] = sum({
            deliv.cfdi: deliv.cfdi_rel.contraprestacion
            for deliv in self.deliveries if deliv.cfdi
            }.values())

        return {"Entregas": data}

    def _set_receptions_complement(self) -> dict:
        recep_cfdis = [cfdi for cfdi in self.cfdis if cfdi.tipoCfdi == "Ingreso"]
        complement = ComplementTypeEnum.ALMACENAMIENTO.value

        reception_complement = self.complement_factory.build_month_complement(
            complement=complement, 
            dictamen=self.dictamen, certificate=self.certificate,
            cfdis=recep_cfdis
            )

        if not reception_complement.get("Complemento"):
            return {
                "TipoComplemento": complement,
                "Aclaracion": "No se cuenta con un CFDI de entrega debido a que la actividad es de Autoconsumo."
            }

        return reception_complement

    def _set_deliveries_complement(self) -> dict:
        complement = ComplementTypeEnum.ALMACENAMIENTO.value
        deliv_cfdis = [cfdi for cfdi in self.cfdis if cfdi.tipoCfdi == "Egreso"]

        delivery_complement = self.complement_factory.build_month_complement(
            complement=complement,
            dictamen=self.dictamen, certificate=self.certificate,
            cfdis=deliv_cfdis
            )

        if not delivery_complement.get("Complemento"):
            return {
                "Complemento": [
                    {
                        "TipoComplemento": complement,
                        "Aclaracion": "No se cuenta con un CFDI de entrega debido a que la actividad es de Autoconsumo."
                        }
                    ]
                }

        return delivery_complement
