from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import OrmBase


class ExistenciaDTanque(OrmBase.Base):
    __tablename__ = 'existencia_d_tanque'

    idExistencia = Column(Integer, primary_key=True)
    idTanque = Column(Integer, ForeignKey('tanque.idTanque'))
    volumenEA = Column(Float, default=0.00)
    volumenAOR = Column(Float, default=0)
    horaRecepcionAcumulado = Column(DateTime)
    volumenExistencias = Column(Float, default=0)
    fechaYHEM=Column(DateTime)
    fechaYHMA=Column(DateTime)

    tanque = relationship("Tanque", backref="existencias")
