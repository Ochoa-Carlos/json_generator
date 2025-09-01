from typing import TypeVar, Optional, Union, Any, Type, List


from json_generator_disp.helpers.logger import logger
from json_generator_disp.models import Cfdi as CfdiModel
from json_generator_disp.models import Dictamen as DictamenModel
from json_generator_disp.models import Certificado as CertificadoModel
from json_generator_disp.services.complements import AlmComplement, ComComplement, DisComplement, ExpComplement, ComplementBase

logging = logger()
# Complement = TypeVar("Complement", bound=ComplementBase)


class ComplementFactory:
    """Complement factory for products."""
    complements = {
        "Almacenamiento": AlmComplement,
        "Comercializacion": ComComplement,
        "Distribucion": DisComplement,
        "Expendio": ExpComplement,
    }

    @staticmethod
    def build_month_complement(complement: str, cfdis: List[CfdiModel],
                               dictamen: Optional[DictamenModel] = None,
                               certificate: Optional[CertificadoModel] = None,
                               ) -> dict:
        """Build monthly complement."""
        complement_class: Type[ComplementBase] = ComplementFactory.complements.get(complement)
        complement_obj = complement_class(
            dictamen=dictamen,
            certificate=certificate,
            cfdis=cfdis,
            )

        return complement_obj.build_complement()
