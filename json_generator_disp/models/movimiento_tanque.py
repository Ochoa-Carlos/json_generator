from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import OrmBase


class MovimientoTanque(OrmBase.Base):
    __tablename__ = 'movimientos_tanque'

    idMovimiento = Column(Integer, primary_key=True, autoincrement=True)
    claveIT = Column(String(20), ForeignKey('tanque.claveIT'))
    cfdi = Column(String(40), ForeignKey('cfdi.cfdi'))
    claveSubProducto = Column(
        String(10), ForeignKey('producto.claveSubProducto'))
    numeroDeRegistro = Column(Integer)
    volumenIT = Column(Float(precision=2), default=0.00)
    volumenFT = Column(Float(precision=2), default=0.00)
    volumenMovimiento = Column(Float(precision=2))
    terminalAlmYDist = Column(String(250))
    permisoAlmYDist = Column(String(30))
    temperatura = Column(Float, default=20)
    presionAbsoluta = Column(Float, default=101.325)
    fechaYHIM = Column(DateTime)
    fechaYHFM = Column(DateTime)
    tipo = Column(String(20), default='Nacional')  # Naciona o internacional
    movimiento = Column(String(20))
    aclaracion = Column(String(600))

    tanque = relationship("Tanque", backref="movimiento_tanque")
    cfdi_rel = relationship("Cfdi", backref="movimiento_tanque")
    producto = relationship("Producto", backref="movimiento_tanque")
