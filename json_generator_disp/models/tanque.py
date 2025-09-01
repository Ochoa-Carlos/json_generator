from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import OrmBase


class Tanque(OrmBase.Base):
    __tablename__ = 'tanque'

    idPermiso = Column(Integer, ForeignKey(
        'permiso.idPermiso'), primary_key=True)
    idProducto = Column(Integer, ForeignKey('producto.idProducto'))
    idTanque = Column(Integer, primary_key=True, autoincrement=True)
    claveIT = Column(String(20))
    locDesTanque = Column(String(260))
    vigenciaCT = Column(Date)
    capacidadTT = Column(Float)
    capacidadOT = Column(Float)
    capacidadFT = Column(Float)
    capacidadGT = Column(Float)
    volumenMO = Column(Float)
    estadoTanque = Column(String(5))
    clave = Column(String(20))

    permiso = relationship("Permiso", backref="tanque")
    producto = relationship("Producto", backref="tanques")
