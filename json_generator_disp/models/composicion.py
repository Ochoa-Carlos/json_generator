from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import OrmBase


class Composicion(OrmBase.Base):
    __tablename__ = 'composicion'

    idProducto = Column(Integer, ForeignKey(
        'producto.idProducto'), primary_key=True)
    idComposicion = Column(Integer, primary_key=True)
    composOG = Column(String(140))
    composDCNFEG = Column(String(110))
    composDCNFED = Column(String(110))
    composDCNFET = Column(String(110))
    composDPEGLP = Column(Float)
    composDBEGLP = Column(Float)
    composDAEP = Column(Float)
    densidadDePetroleo = Column(Float)
    poderCalorifico = Column(Float)
    Cc1 = Column(Float)
    Cc2 = Column(Float)
    Cc3 = Column(Float)
    Cc4 = Column(Float)
    Cc5 = Column(Float)
    Cc6 = Column(Float)
    Cc7 = Column(Float)
    Cc8 = Column(Float)
    Cc9 = Column(Float)
    Cc10 = Column(Float)
    Pcc1 = Column(Float)
    Pcc2 = Column(Float)
    Pcc3 = Column(Float)
    Pcc4 = Column(Float)
    Pcc5 = Column(Float)
    Pcc6 = Column(Float)
    Pcc7 = Column(Float)
    Pcc8 = Column(Float)
    Pcc9 = Column(Float)
    Pcc10 = Column(Float)

    producto = relationship(
        'Producto', back_populates='composiciones', overlaps="composiciones")
