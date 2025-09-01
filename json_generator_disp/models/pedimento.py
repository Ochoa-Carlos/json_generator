from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import OrmBase


class Pedimento(OrmBase.Base):
    __tablename__ = 'pedimento'

    idPedimento = Column(Integer, primary_key=True)
    idPermiso = Column(Integer, ForeignKey('permiso.idPermiso'))
    puntoDIOE = Column(String(10))
    paisOOD = Column(String(10))
    medioDTEOSA = Column(String(10))
    pedimentoAduanal = Column(String(25))
    incoterms = Column(String(10))
    precioDIOE = Column(Float(14, 2))
    volumenD = Column(Float(14, 2))
    fechaI = Column(Date)
    fechaF = Column(Date)

    permiso = relationship("Permiso", backref="pedimentos")
