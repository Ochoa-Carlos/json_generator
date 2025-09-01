from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import OrmBase


class Dictamen(OrmBase.Base):
    __tablename__ = 'dictamen'

    idDictamen = Column(Integer, primary_key=True, autoincrement=True)
    claveIdentificacion = Column(String)
    rfcDictamen = Column(String(20))
    loteDictamen = Column(String(30))
    numeroFD = Column(String(310))
    fechaED = Column(Date)
    resultadoDictamen = Column(String(310))
    tomaMuestra = Column(Date)
