from typing import Any, List, Dict
from sqlalchemy.orm import Session
from json_generator_disp.models import Producto, MovimientoTanque, MovimientoDispensario, ExistenciaDTanque, MedidorDispensario, Dictamen, Certificado, Tanque, Dispensario

class DbRepository:
    """Repo class for db querying."""

    def __init__(self, db: Session):
        """Set db session."""
        self._db = db

    def get_products(self) -> List[Producto]:
        """Return all producs in db."""
        return self._db.query(Producto).all()

    def get_receptions(self, from_date: str, to_date: str) -> List[MovimientoTanque]:
        """Return all receptionss in db."""
        return self._db.query(MovimientoTanque).filter(
            MovimientoTanque.fechaYHIM >= from_date,
            MovimientoTanque.fechaYHIM <= to_date
        ).all()

    def get_deliveries(self, from_date: str, to_date: str) -> List[MovimientoDispensario]:
        """Return all delivieres in db."""
        return self._db.query(MovimientoDispensario).filter(
            MovimientoDispensario.fechaYHM >= from_date,
            MovimientoDispensario.fechaYHM <= to_date
        ).all()

    def get_existances(self, from_date: str, to_date: str) -> List[ExistenciaDTanque]:
        """Return all existances in db."""
        return self._db.query(ExistenciaDTanque).filter(
            ExistenciaDTanque.fechaYHEM >= from_date,
            ExistenciaDTanque.fechaYHEM <= to_date
        ).all()

    def get_deliveries(self, from_date: str, to_date: str) -> List[MovimientoDispensario]:
        """Retrieve records from movimiento_dispensario table according model in range of date."""
        return self._db.query(MovimientoDispensario).filter(
            MovimientoDispensario.fechaYHM >= from_date,
            MovimientoDispensario.fechaYHM <= to_date
        ).all()

    def get_disp_medidores(self) -> List[MedidorDispensario]:
        """Retrieve all MedidoresDispensario.
        :return: List of MedidoresDispensario objs."""
        return self._db.query(MedidorDispensario).all()

    def get_tanks(self) -> List[Tanque]:
        """Retreive all tanques.
        :return: List of Tanque objs."""
        return self._db.query(Tanque).all()

    def get_tanks_by_product(self, product_id: int) -> List[Tanque]:
        """Retreive all tanques.
        :return: List of Tanque objs."""
        return self._db.query(Tanque).filter(Tanque.idProducto == product_id).all()

    def get_dispensarios(self) -> List[Dispensario]:
        """Retreive all dispensaries.
        :return: List of Dispensario objs."""
        return self._db.query(Dispensario).all()

    def get_dictamen(self) -> Dictamen:
        """Retreive the first encountered dictamen.
        :return: Dictamen obj."""
        return self._db.query(Dictamen).first()

    def get_certificate(self) -> Certificado:
        """Retreive the first encountered certificado.
        :return: Certificado obj."""
        return self._db.query(Certificado).first()
    
    def get_day_existance(self, from_date: str, to_date: str) -> ExistenciaDTanque:
        """Return TanqueExistance record of a specific day."""
        return self._db.query(ExistenciaDTanque).filter(
            ExistenciaDTanque.fechaYHEM >= from_date,
            ExistenciaDTanque.fechaYHEM <= to_date
        ).first()
