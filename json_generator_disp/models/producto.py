from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import OrmBase


class Producto(OrmBase.Base):

    __tablename__ = 'producto'

    idPermiso = Column(Integer, ForeignKey(
        'permiso.idPermiso'), primary_key=True)
    idProducto = Column(Integer, primary_key=True)
    idCertificado = Column(Integer, ForeignKey('certificado.idCertificado'))
    claveProducto = Column(String(10))
    claveSubProducto = Column(String(10))
    gasolinaCCNF = Column(String(5))
    dieselCCNF = Column(String(5))
    turbosinaCCNF = Column(String(5))
    otros = Column(String(30))
    marcaComercial = Column(String(210))
    marcaje = Column(String(50))
    concentracionSustanciaMarcaje = Column(Integer)
    gasNaturalOCondensados = Column(String(10))
    fraccionMolar = Column(Float)
    unidadMedida = Column(String(10))
    UnidadEnergia = Column(String(10))

    permiso = relationship('Permiso', backref='producto')
    certificado = relationship("Certificado", backref="producto")
    composiciones = relationship('Composicion', back_populates='producto')
