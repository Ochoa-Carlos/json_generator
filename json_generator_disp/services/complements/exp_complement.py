from datetime import datetime
from typing import Union, Optional, Any, List
from json_generator.helpers.enumerators import ComplementTypeEnum
from json_generator.models import Cfdi as CfdiModel
from json_generator.models import Dictamen as DictamenModel
from json_generator.models import Certificado as CertificadoModel
from .complement_base import ComplementBase


class ExpComplement(ComplementBase):
    """Complement Expendio build class."""
    def __init__(self, dictamen: Optional[DictamenModel], certificate: Optional[CertificadoModel],
                 cfdis: List[CfdiModel]
                 ):
        self.dictamen = dictamen
        self.certificate = certificate
        self.cfdis = cfdis

    def build_complement(self):
        """Build Almacenamiento complement."""
        print("=================>BUILD EXPENDIO COMPLEMETN<=================")
        complement_list = []
        for cf_index, _ in enumerate(self.cfdis):
            complement_dict = {"TipoComplemento": ComplementTypeEnum.EXPENDIO.value}

            complement_dict.update(self._set_terminal_alm_dist(cf_index=cf_index))
            complement_dict.update(self._set_dictamen())
            complement_dict.update(self._set_certificado())
            complement_dict.update(self._set_national(cf_index=cf_index))
            complement_dict.update(self._set_extranjero(cf_index=cf_index))
            complement_dict.update(self._set_aclaracion())

            complement_list.append(complement_dict)

        return {"Complemento": complement_list}

# TODO TerminalAlmYDist Almacenamiento
# TODO TerminalAlmYDist Transporte
    def _set_terminal_alm_dist(self, cf_index: int) -> dict:
        """build key TerminalAlmYDist"""
        alm_data = {}
        tran_data = {}
        if not all(mov.terminalAlmYDist for mov in self.cfdis[cf_index].movimiento_tanque):
            return {}

        if terminal_alm_dist := self.cfdis[cf_index].movimiento_tanque[0].terminalAlmYDist:
            alm_data["TerminalAlmYDist"] = terminal_alm_dist
        alm_data["PermisoAlmYDist"] = self.cfdis[cf_index].movimiento_tanque[0].permisoAlmYDist
        if tarifa_almac := self.cfdis[cf_index].tarifaDT:
            alm_data["TarifaDeAlmac"] = tarifa_almac

        return {"TerminalAlmYDist": {
            **({"Almacenamiento": alm_data} if alm_data else {}),
            **({"Transporte": tran_data} if tran_data else {})
        }}

    def _set_dictamen(self) -> dict:
        """build key Dictamen"""
        dictamen_data = {}

        if self.dictamen is None:
            return {}

        dictamen_data["RfcDictamen"] = self.dictamen.rfcDictamen
        dictamen_data["LoteDictamen"] = self.dictamen.loteDictamen
        dictamen_data["NumeroFolioDictamen"] = self.dictamen.numeroFD
        dictamen_data["FechaEmisionDictamen"] = self.dictamen.fechaED
        dictamen_data["ResultadoDictamen"] = self.dictamen.resultadoDictamen

        return {"Dictamen": dictamen_data}

# TODO Certificado
    def _set_certificado(self) -> dict:
        """build key Certificado"""
        cert_data = {}

        if self.certificate is None:
            return {}

        cert_data["RfcCertificado"] = self.certificate.rfcCertificado
        cert_data["NumeroFolioCertificado"] = self.certificate.nFolioCertificado
        cert_data["FechaEmisionCertificado"] = self.certificate.fechaEmisionCertificado
        cert_data["ResultadoCertificado"] = self.certificate.resultadoCertificado

        return {"Certificado": cert_data}

# TODO Nacional
# TODO Cfdi: PrecioDeVentaAlPublico
# TODO Cfdi: PrecioVenta
    def _set_national(self, cf_index: int) -> dict:
        """build key Nacional"""
        nat_data = {}
        cfdi_data = {}
        if self.cfdis is None:
            return {}

        nat_data["RfcClienteOProveedor"] = self.cfdis[cf_index].rfcCliente
        nat_data["NombreClienteOProveedor"] = self.cfdis[cf_index].nombreCliente
        # nat_data["PermisoProveedor"] =
        cfdi_data["Cfdi"] = self.cfdis[cf_index].cfdi
        cfdi_data["TipoCfdi"] = self.cfdis[cf_index].tipoCfdi
        cfdi_data["PrecioCompra"] = self.cfdis[cf_index].contraprestacion
        if self.cfdis[cf_index].tipoCfdi == "Ingreso":
            cfdi_data["PrecioDeVentaAlPublico"] = 0
        if self.cfdis[cf_index].tipoCfdi == "Ingreso":
            cfdi_data["PrecioVenta"] = self.cfdis[cf_index].contraprestacion
        cfdi_data["FechaYHoraTransaccion"] = self.cfdis[cf_index].fechaYHT.strftime("%Y-%m-%dT%H:%M:%S%z-06:00")
        cfdi_data["VolumenDocumentado"] = {
            "ValorNumerico": self.cfdis[cf_index].volumenD,
            "UnidadDeMedida": self.cfdis[cf_index].movimiento_tanque[0].producto.unidadMedida,
        }

        nat_data["CFDIs"] = [cfdi_data]

        return {"Nacional": [nat_data]}

# TODO Extranjero
    def _set_extranjero(self, cf_index: int) -> dict:
        """build key Extranjero"""
        return {}

    def _set_aclaracion(self) -> dict:
        """build key Aclaracion"""
        if self.cfdis:
            return {}

        return {"Aclaracion": "En reporte mensual, no se cuenta con CFDIs asociados a las Entregas ya que se trata de permiso de Almacenamiento para Autoconsumo"}
