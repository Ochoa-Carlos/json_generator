from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base
from json_generator_disp.models.base import OrmBase

class Cfdi(OrmBase.Base):
    __tablename__ = 'cfdi'


    cfdi = Column(String(40), primary_key=True)
    rfcCliente = Column(String(20))
    nombreCliente = Column(String(150))
    tipoCfdi = Column(String(10))
    contraprestacion = Column(Float)
    tarifaDT = Column(Float)
    cargoPCDT = Column(Float)
    cargoPUT = Column(Float)
    cargoVT = Column(Float)
    descuento = Column(Float)
    fechaYHT = Column(DateTime)
    volumenD = Column(Float)
