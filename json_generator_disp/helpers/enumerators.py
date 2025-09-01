from enum import Enum


class TipoCfdi(Enum):
    INGRESO = "Ingreso"
    EGRESO = "Egreso"
    TRASLADO = "Traslado"

class CaracterEnum(Enum):
    """Caracter Enum."""
    PERMISIONARIO = ["modalidadPermiso", "numPermiso"]
    ASIGNATARIO = ["numContratoOAsignacion"]
    CONTRATISTA = ["numContratoOAsignacion"]
    USUARIO = ["instalacionAlmacenGasNatural"]

class ComplementTypeEnum(Enum):
    """Complemento Enum."""
    ALMACENAMIENTO = "Almacenamiento"
    CDLR = "CDLR"
    COMERCIALIZACION = "Comercializacion"
    DISTRIBUCION = "Distribucion"
    EXPENDIO = "Expendio"
    EXTRACCION = "Extraccion"
    REFINACION = "Refinacion"
    TRANSPORTE = "Transporte"

class SiNoEnum(Enum):
    """Si No Enum"""
    SI = "Sí"
    NO = "No"

class ProductKeyEnum(Enum):
    """ClaveProducto Enum"""
    PR03 = "PR03"
    PR07 = "PR07"
    PR08 = "PR08"
    PR09 = "PR09"
    PR10 = "PR10"
    PR11 = "PR11"
    PR12 = "PR12"
    PR13 = "PR13"
    PR14 = "PR14"
    PR15 = "PR15"
    PR16 = "PR16"
    PR17 = "PR17"
    PR18 = "PR18"
    PR19 = "PR19"
