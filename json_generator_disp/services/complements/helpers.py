from datetime import datetime
from typing import TypeVar, Optional, Union
from json_generator.services.complements import AlmComplement, ComComplement, DisComplement, ComplementBase
from json_generator.models import MovimientoTanque

Complement = TypeVar("Complement", bound=ComplementBase)
complements = {
    "Almacenamiento": AlmComplement,
    "Comercializacion": ComComplement,
    "Distribucion": DisComplement,
    }


class ComplementBuilder:
    """Complement builder."""
    def __init__(self, complement: str, movements: Optional[MovimientoTanque],
                 db_name: str, date: Union[str, datetime]) -> dict:
        """Complement init."""
        self.complement: Complement = complements.get(complement)(
            movements=movements,
            db_name=db_name,
            date=date
        )

    def build_month_complement(self) -> dict:
        """Build complement"""
        print("SELF COMPLEMENTO", self.complement)
        print("llego al builder del complemento")
        self.complement.build_complement()
