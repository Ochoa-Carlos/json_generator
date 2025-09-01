from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import OrmBase


class Manguera(OrmBase.Base):
    __tablename__ = 'manguera'

    idManguera = Column(Integer, primary_key=True, autoincrement=True)
    idDispensario = Column(Integer, ForeignKey('dispensario.idDispensario'), nullable=False)
    claveIM = Column(String(100), nullable=False)
    idProducto = Column(Integer, ForeignKey('producto.idProducto'), nullable=False)

    producto = relationship("Producto", backref="producto_rel")
    # dispensario_rel = relationship("Dispensario", backref="manguera")
    # medidor_dispensario = relationship("MedidorDispensario", backref="manguera")
    dispensario = relationship("Dispensario", back_populates="mangueras")
