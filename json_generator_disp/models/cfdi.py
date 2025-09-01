from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.orm import relationship
from .base import OrmBase


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
    precioU = Column(Float)
    #permisoProveedor = Column(String(150))

    # movimientos = relationship("MovimientoTanque", backref="cfdis")

    def __repr__(self):
        return f"""
            Cfdi(cfdi={self.cfdi},
            rfcCliente={self.rfcCliente}, 
            nombreCliente={self.nombreCliente}, 
            tipoCfdi={self.tipoCfdi}, 
            contraprestacion={self.contraprestacion}, 
            tarifaDT={self.tarifaDT}, 
            cargoPCDT={self.cargoPCDT}, 
            cargoPUT={self.cargoPUT}, 
            cargoVT={self.cargoVT}, 
            descuento={self.descuento}, 
            fechaYHT={self.fechaYHT}, volumenD={self.volumenD})
            """
