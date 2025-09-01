from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import OrmBase


# class Dispensario(OrmBase.Base):
#     __tablename__ = 'dispensario'

#     idDispensario = Column(Integer, primary_key=True, autoincrement=True)
#     idPermiso = Column(Integer, nullable=False)
#     idProducto = Column(Integer, nullable=False)
#     claveDispensario = Column(String(50), nullable=False)
#     descripcion = Column(String(255), nullable=False)
#     clave = Column(String(50), nullable=False)

class Dispensario(OrmBase.Base):
    __tablename__ = 'dispensario'

    idDispensario = Column(Integer, primary_key=True, autoincrement=True)
    claveID = Column(String(10), nullable=True, unique=True)

    # manguera_rel = relationship("Manguera", backref="dispensario")
    mangueras = relationship("Manguera", back_populates="dispensario")
