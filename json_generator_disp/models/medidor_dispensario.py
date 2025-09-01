from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import OrmBase


class MedidorDispensario(OrmBase.Base):
    __tablename__ = 'medidor_dispensario'

    idMedidor = Column(Integer, primary_key=True, autoincrement=True)
    idManguera = Column(Integer, ForeignKey('manguera.idManguera'), nullable=False)
    sistemaMT = Column(String(100), nullable=False)
    localizODSMT = Column(String(255), nullable=False)
    vigenciaCSMT = Column(Date, nullable=False)
    incertidumbreMSMT = Column(Float, nullable=True)

    manguera = relationship("Manguera", backref="medidor_dispensario")
