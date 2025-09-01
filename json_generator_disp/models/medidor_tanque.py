from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import OrmBase


class MedidorTanque(OrmBase.Base):
    __tablename__ = 'medidor_tanque'

    idTanque = Column(Integer, ForeignKey('tanque.idTanque'))
    idMedidor = Column(Integer, primary_key=True, autoincrement=True)
    sistemaMT = Column(String(20))
    localizODSMT = Column(String(260))
    VigenciaCSMT = Column(Date)
    incertidumbreMSMT = Column(Float)

    tanque = relationship("Tanque", backref="medidor_tanque")
