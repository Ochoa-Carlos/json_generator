from datetime import datetime
from typing import Union, Optional, Any, List, Dict
from json_generator_disp.helpers.enumerators import ComplementTypeEnum
from json_generator_disp.models import Cfdi as CfdiModel
from json_generator_disp.models import Dictamen as DictamenModel
from json_generator_disp.models import Certificado as CertificadoModel
from .complement_base import ComplementBase
from json_generator_disp.helpers.enumerators import TipoCfdi
from .constants import RFC_REGEX, PERMISO_PROVEEDOR_REGEX, CFDI_REGEX, DATE_ISO8601_REGEX
class Transporte:
    """Build Transporte Key Complement."""
    def __init__(self, cfdis: List[CfdiModel]):
        self.cfdis = cfdis
        
    def build(self) -> Any:
        """Build list of Transporte objects."""
        tran_data = {}
        # if not all(mov.terminalAlmYDist for mov in self.cfdis[self.cf_index].movimiento_tanque):
        #     return []
            
        raise NotImplementedError
        return tran_data


class Dictamen:
    """Build Dictamen Key Complement."""
    def __init__(self, dictamen: Optional[DictamenModel]):
        self.dictamen = dictamen
        
    def build(self) -> List[Dict[str, Dict]]:
        """Build list of Dictamen objects."""
        if self.dictamen is None:
            return []

        dictamen_complement = [
            {
                "TipoComplemento": ComplementTypeEnum.ALMACENAMIENTO.value,
                "Dictamen": 
                {
                    "RfcDictamen": self.dictamen.rfcDictamen,
                    "LoteDictamen": self.dictamen.loteDictamen,
                    "NumeroFolioDictamen": self.dictamen.numeroFD,
                    "FechaEmisionDictamen": self.dictamen.fechaED.isoformat(),
                    "ResultadoDictamen": self.dictamen.resultadoDictamen
                }
            }
        ]

        return dictamen_complement


class Certificado:
    """Build Certificado Key Complement."""
    def __init__(self, certificado: Optional[CertificadoModel]):
        self.certificado = certificado
        
    def build(self) -> List[Dict[str, List]]:
        """Build list of Certificado objects."""
        if self.certificado is None:
            return []
            
        certificate_data = [
            {
                "TipoComplemento": ComplementTypeEnum.ALMACENAMIENTO.value,
                "Certificado": [
                    {
                        "RfcCertificado": self.certificado.rfcCertificado,
                        "NumeroFolioCertificado": self.certificado.nFolioCertificado,
                        "FechaEmisionCertificado": self.certificado.fechaEmisionCertificado,
                        "ResultadoCertificado": self.certificado.resultadoCertificado
                    }
                ]
            }
        ]

        return certificate_data


class Nacional:
    """Build National Key Complement."""
    def __init__(self, cfdis: List[CfdiModel]):
        self.cfdis = cfdis
        
    def build(self) -> List[Dict]:
        """Build list of National CFDIs objects."""
        # national_complement = []
        if self.cfdis is None:
            return []

        national_complement = [
            {
                "TipoComplemento": ComplementTypeEnum.ALMACENAMIENTO.value,
                "Nacional": [
                    {
                        "RfcClienteOProveedor": cfdi.rfcCliente,
                        "NombreClienteOProveedor": cfdi.nombreCliente,
                        "CFDIs": [
                            {
                                "Cfdi": cfdi.cfdi,
                                "TipoCfdi": cfdi.tipoCfdi,
                                "Contraprestacion": cfdi.contraprestacion,
                                "FechaYHoraTransaccion": cfdi.fechaYHT.strftime("%Y-%m-%dT%H:%M:%S-06:00"),
                                "VolumenDocumentado": {
                                    "ValorNumerico": cfdi.volumenD,
                                    "UnidadMedida": cfdi.movimiento_tanque[0].producto.unidadMedida
                                }
                            }
                        ]
                    }
                ]
            } for cfdi in self.cfdis
        ]

        validations = Validator(VALIDACIONES_NACIONAL)
        validations.validate(data=national_complement)

        return national_complement


class Extranjero:
    """Build Extranjero Key Complement."""
    def __init__(self, cfdis: List[CfdiModel]):
        self.cfdis = cfdis
        
    def build(self) -> Dict:
        """Build list of Extranjero objects."""
        raise NotImplementedError
        return []


class Aclaracion:
    """Build Aclaracion Key Complement."""
    def __init__(self, cfdis: List[CfdiModel]):
        self.cfdis = cfdis
        
    def build(self) -> Dict:
        """Build list of Aclaracion object."""
        if self.cfdis:
            return []

        aclaracion_data = [
            {
                "TipoComplemento": ComplementTypeEnum.ALMACENAMIENTO.value,
                "Aclaracion": "En reporte mensual, no se cuenta con CFDIs asociados a las Entregas ya que se trata de permiso de Almacenamiento para Autoconsumo"
            }
        ]

        return aclaracion_data

class AlmComplement(ComplementBase):
    """Complement Almacenamiento build class."""
    def __init__(self, dictamen: Optional[DictamenModel],
                 certificate: Optional[CertificadoModel], cfdis: Optional[List[CfdiModel]]):
        self.dictamen = dictamen
        self.certificate = certificate
        self.cfdis = cfdis
        
    def build_complement(self) -> Dict[str, List]:
        """Build Almacenamiento complement."""
        print("=================>BUILD ALMACENAMIENTO COMPLEMENT<=================")
        alm_complement = []
        
        # transporte = Transporte(self.cfdis)
        dictamen = Dictamen(self.dictamen)
        certificado = Certificado(self.certificate)
        nacional = Nacional(self.cfdis)
        # extranjero = Extranjero(self.cfdis)
        aclaracion = Aclaracion(self.cfdis)
        
        # alm_complement.extend(transporte.build())
        alm_complement.extend(dictamen.build())
        alm_complement.extend(certificado.build())
        alm_complement.extend(nacional.build())
        # alm_complement.extend(extranjero.build())
        alm_complement.extend(aclaracion.build())

        return {"Complemento": alm_complement}


class Validator:
    def __init__(self, validations):
        self.validations = validations
        self.errors = []

    def validate(self, data, prefix= ""):
        if isinstance(data, dict):
            for key, value in data.items():
                current_key = key
                # current_key = f"{prefix}.{key}" if prefix else key
                if current_key in self.validations:
                    self._apply_validations(field=key, value=value)

                if isinstance(value, (dict, list)):
                    self.validate(data=value, prefix=current_key)
        
        elif isinstance(data, list):
            for index, item in enumerate(data):
                current_key = f"{prefix}[{index}]"
                self.validate(data=item, prefix=current_key)

        return len(self.errors) == 0, self.errors

    def _apply_validations(self, field, value):
        """Aplica las validation de validación para un campo específico."""
        validations = self.validations.get(field, [])
        
        for validation in validations:
            if "type" in validation and not isinstance(value, validation["type"]):
                self.errors.append(f"Campo {field}: se esperaba {validation['type'].__name__}, se recibió {type(value).__name__}")

            if "min_lenght" in validation and isinstance(value, int) and len(value) < validation["min_lenght"]:
                self.errors.append(f"Campo {field}: no cumple con la longitud minima {validation['min_lenght']}")

            if "max_lenght" in validation and isinstance(value, int) and len(value) > validation["max_lenght"]:
                self.errors.append(f"Campo {field}: no cumple con la longitud maxima {validation['max_lenght']}")

            if "min_val" in validation and value < validation["min_val"]:
                self.errors.append(f"Campo {field}: no cumple con la longitud minima {validation['min_val']}")

            if "max_val" in validation and value > validation["max_val"]:
                self.errors.append(f"Campo {field}: no cumple con la longitud maxima {validation['max_val']}")
            
            if "regex" in validation and isinstance(value, str):
                import re
                if not re.match(validation["regex"], value):
                    self.errors.append(f"field {field}: no cumple con el patrón requerido")

            if "allowed_values" in validation and isinstance(value, str):
                if value not  in validation["allowed_values"]:
                    self.errors.append(f"field {field}: no tiene un valor permitido.")


VALIDACIONES_NACIONAL = {
    "RfcClienteOProveedor": [
        {"type": str, "presence": True, "regex": RFC_REGEX, "min_lenght": 12, "max_lenght": 13},
        {"mensaje": "RfcClienteOProveedor no válido."}
    ],
    "NombreClienteOProveedor": [
        {"type": str, "presence": True, "min_lenght": 10, "max_lenght": 150},
        {"mensaje": "NombreClienteOProveedor no válido."}
    ],
    "PermisoProveedor": [
        {"type": str, "presence": False, "regex": PERMISO_PROVEEDOR_REGEX},
        {"mensaje": "PermisoProveedor no valido."}
    ],
    "Cfdi": [
        {"type": str, "presence": True, "regex": CFDI_REGEX},
        {"mensaje": "CFDI no válido."}
    ],
    "TipoCfdi": [
        {"type": str, "presence": True, "allowed_values": [enum for enum in TipoCfdi._value2member_map_]},
        {"mensaje": "TipoCfdi no válido."}
    ],
    "PrecioCompra": [
        {"type": float, "presence": False, "min_val": 0, "max_val": 1000000000000},
        {"mensaje": "PrecioCompra no válido."}
    ],
    "Contraprestacion": [
        {"type": float, "presence": False, "min_val": 0, "max_val": 1000000000000},
        {"mensaje": "Contraprestacion no válido."}
    ],
    "TarifaDeAlmacenamiento": [
        {"type": float, "presence": False, "min_val": 0, "max_val": 1000000000000},
        {"mensaje": "TarifaDeAlmacenamiento no válido."}
    ],
    "CargoPorCapacidadAlmac": [
        {"type": float, "presence": False, "min_val": 0, "max_val": 1000000000000},
        {"mensaje": "CargoPorCapacidadAlmac no válido."}
    ],
    "CargoPorUsoAlmac": [
        {"type": float, "presence": False, "min_val": 0, "max_val": 1000000000000},
        {"mensaje": "CargoPorUsoAlmac no válido."}
    ],
    "CargoVolumetricoAlmac": [
        {"type": float, "presence": False, "min_val": 0, "max_val": 1000000000000},
        {"mensaje": "CargoVolumetricoAlmac no válido."}
    ],
    "Descuento": [
        {"type": float, "presence": False, "min_val": 0, "max_val": 1000000000000},
        {"mensaje": "Descuento no válido."}
    ],
    "FechaYHoraTransaccion": [
        {"type": str, "presence": True, "regex": DATE_ISO8601_REGEX},
        {"mensaje": "FechaYHoraTransaccion no válido."}
    ],
}