from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import OrmBase


class ExistenciaMTanque(OrmBase.Base):
    __tablename__ = 'existencia_m_tanque'

    idExistencia = Column(Integer, primary_key=True, autoincrement=True)
    idTanque = Column(Integer, ForeignKey('tanque.idTanque'))
    totalRecepciones = Column(Integer)
    sumaVolumenRecepcion = Column(Float)
    importeTotalRecepciones = Column(Float)
    totalEntregas = Column(Integer)
    sumaVolumenEntregado = Column(Float)
    importeTotalEntregas = Column(Float)
    totalDocumentos = Column(Integer)
    FechaYHRM = Column(DateTime)

    tanque = relationship("Tanque", backref="existencia_m_tanque")
