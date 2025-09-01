from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import OrmBase


class MedidorDucto(OrmBase.Base):
    __tablename__ = 'medidor_ducto'

    idMedidor = Column(Integer, primary_key=True, autoincrement=True)
    idDucto = Column(Integer, ForeignKey('ducto.idDucto'))
    sistemaMD = Column(String(20))
    localizODSMD = Column(String(260))
    VigenciaCSMD = Column(Date)
    incertidumbreMSMD = Column(Float)

    ducto = relationship("Ducto", backref="medidor_ducto")
