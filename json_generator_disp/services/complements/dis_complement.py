from datetime import datetime
from typing import Union, Optional, Any, List
from json_generator.helpers.enumerators import ComplementTypeEnum
from json_generator.models import Cfdi as CfdiModel
from json_generator.models import Dictamen as DictamenModel
from json_generator.models import Certificado as CertificadoModel
from .complement_base import ComplementBase


class DisComplement(ComplementBase):
    """Complement Distribucion build class."""
    def __init__(self, dictamen: Optional[DictamenModel], certificate: Optional[CertificadoModel],
                 cfdis: List[CfdiModel]
                 ):
        self.dictamen = dictamen
        self.certificate = certificate
        self.cfdis = cfdis

    def build_complement(self):
        """Build Almacenamiento complement."""
        print("=================>BUILD DISTRIBUCION COMPLEMETN<=================")
        complement_list = []
        for cf_index, _ in enumerate(self.cfdis):
            complement_dict = {"TipoComplemento": ComplementTypeEnum.DISTRIBUCION.value}

            complement_dict.update(self._set_terminal_alm_trans(cf_index=cf_index))
            complement_dict.update(self._set_dictamen())
            complement_dict.update(self._set_national(cf_index=cf_index))
            complement_dict.update(self._set_extranjero())
            complement_dict.update(self._set_aclaracion())

            complement_list.append(complement_dict)

        return {"Complemento": complement_list}

# TODO TerminalAlmYTrans Almacenamiento
# TODO TerminalAlmYTrans Transporte
    def _set_terminal_alm_trans(self, cf_index: int) -> dict:
        """build key TerminalAlmYDist"""
        if not all(mov.permisoAlmYDist for mov in self.cfdis[cf_index].movimiento_tanque):
            return {}

    def _set_dictamen(self) -> dict:
        """build key Dictamen"""
        if self.dictamen is None:
            return {}

        dictamen_data = {}
        dictamen_data["RfcDictamen"] = self.dictamen.rfcDictamen
        dictamen_data["LoteDictamen"] = self.dictamen.loteDictamen
        dictamen_data["NumeroFolioDictamen"] = self.dictamen.numeroFD
        dictamen_data["FechaEmisionDictamen"] = self.dictamen.fechaED
        dictamen_data["ResultadoDictamen"] = self.dictamen.resultadoDictamen

        return {"Dictamen": dictamen_data}

# TODO Nacional
# TODO Nacional: PermisoClienteOProveedor
    def _set_national(self, cf_index: int) -> dict:
        """build key Nacional"""
        nat_data = {}
        cfdi_data = {}
        if self.cfdis is None:
            return {}

        nat_data["RfcClienteOProveedor"] = self.cfdis[cf_index].rfcCliente
        nat_data["NombreClienteOProveedor"] = self.cfdis[cf_index].nombreCliente
        # nat_data["PermisoClienteOProveedor"] = SomeDataHere
        cfdi_data["Cfdi"] = self.cfdis[cf_index].cfdi
        cfdi_data["TipoCfdi"] = self.cfdis[cf_index].tipoCfdi
        cfdi_data["PrecioVentaOCompraContrap"] = self.cfdis[cf_index].contraprestacion
        cfdi_data["FechaYHoraTransaccion"] = self.cfdis[cf_index].fechaYHT.strftime("%Y-%m-%dT%H:%M:%S%z-06:00")
        cfdi_data["VolumenDocumentado"] = {
            "ValorNumerico": self.cfdis[cf_index].volumenD,
            "UnidadDeMedida": self.cfdis[cf_index].movimiento_tanque[0].producto.unidadMedida,
        }

        nat_data["CFDIs"] = [cfdi_data]

        return {"Nacional": [nat_data]}

# TODO Extranjero
    def _set_extranjero(self) -> dict:
        """build key Extranjero"""
        return {}

    def _set_aclaracion(self) -> dict:
        """build key Aclaracion"""
        if self.cfdis:
            return {}

        return {"Aclaracion": "En reporte mensual, no se cuenta con CFDIs asociados a las Entregas ya que se trata de permiso de Almacenamiento para Autoconsumo"}
