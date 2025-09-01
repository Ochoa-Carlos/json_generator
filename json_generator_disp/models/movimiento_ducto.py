from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import OrmBase


class MovimientoDucto(OrmBase.Base):
    __tablename__ = 'movimientos_ducto'

    idMovimiento = Column(Integer, primary_key=True, autoincrement=True)
    claveID = Column(String(20), ForeignKey('ducto.claveID'))
    cfdi = Column(String(40), ForeignKey('cfdi.cfdi'))
    claveSubProducto = Column(
        String(10), ForeignKey('producto.claveSubProducto'))
    numeroDeRegistro = Column(Integer)
    volumenPunto = Column(Float(precision=2), default=0.00)
    volumen = Column(Float(precision=2), default=0.00)
    temperatura = Column(Float)
    presionAbsoluta = Column(Float)
    tipo = Column(String(20), default='Nacional')  # Nacional o internacional
    movimiento = Column(String(20))
    aclaracion = Column(String(600))
    fechaYHIM = Column(DateTime)
    fechaYHFM = Column(DateTime)

    ducto = relationship("Ducto", backref="movimiento_ducto")
    cfdi_rel = relationship("Cfdi", backref="movimiento_ducto")
    producto = relationship("Producto", backref="movimiento_ducto")
