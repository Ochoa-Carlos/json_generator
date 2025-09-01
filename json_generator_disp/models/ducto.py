from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import OrmBase


class Ducto(OrmBase.Base):
    __tablename__ = 'ducto'

    idDucto = Column(Integer, primary_key=True)
    idProducto = Column(Integer, ForeignKey('producto.idProducto'))
    claveID = Column(String(20))
    descripcionDucto = Column(String(260))
    diametroDucto = Column(Float)
    capacidadGT = Column(Float)
    clave = Column(String(20))

    producto = relationship("Producto", backref="ductos")
