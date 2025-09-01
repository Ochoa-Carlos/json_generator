from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, DECIMAL, Index
from sqlalchemy.orm import relationship
from .base import OrmBase
from datetime import datetime


class MovimientoDispensario(OrmBase.Base):
    __tablename__ = 'movimientos_dispensario'

    idMovimiento = Column(Integer, primary_key=True, autoincrement=True)
    claveIDispensario = Column(String(50),  ForeignKey('dispensario.claveID'))
    claveManguera = Column(String(50), nullable=False)
    cfdi = Column(String(40),ForeignKey('cfdi.cfdi'))
    claveSubProducto = Column(String(10), ForeignKey('producto.claveSubProducto'))
    numeroDeRegistro = Column(Integer, nullable=False)
    tipoR = Column(String(10), nullable=False)
    volumenET = Column(Float, nullable=False)
    volumenI = Column(Float, nullable=False)
    fechaYHM = Column(DateTime,  default=datetime.utcnow)
    tipo = Column(String(20), nullable=True)
    movimiento = Column(String(20), nullable=True)
    aclaracion = Column(Text, nullable=True)


    dispensario = relationship("Dispensario", backref="movimiento_dispensario")
    cfdi_rel = relationship("Cfdi", backref="movimiento_dispensario")
    producto = relationship("Producto", backref="movimiento_dispensario")

# class MovimientoDispensario(OrmBase.Base):
#     __tablename__ = 'movimientos_dispensario'

#     idMovimiento = Column(Integer, primary_key=True, autoincrement=True)
#     claveID = Column(String(20), ForeignKey('dispensario.claveID'))
#     cfdi = Column(String(40), ForeignKey('cfdi.cfdi'))
#     claveSubProducto = Column(String(10), ForeignKey('producto.claveSubProducto'))
#     numeroDeRegistro = Column(Integer)
#     tipoR = Column(String(20), default='Nacional')
#     volumenETA = Column(Float, default=0.00) #VolumenEntregadoAcumulado
#     volumenETI = Column(Float, default=0.00) #VolumenEntregadoInstantaneo
#     fechaYHM = Column(DateTime)
#     tipo = Column(String(20), default='Nacional')
#     movimiento = Column(String(20))
#     aclaracion = Column(String(600))

#     dispensario_rel = relationship("Dispensario", backref="movimiento_dispensario_rel", foreign_keys=[claveID])
#     cfdi_rel = relationship("Cfdi", backref="movimientos_dispensario", foreign_keys=[cfdi])
#     producto = relationship("Producto", backref="dispensario")
