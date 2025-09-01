from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from .base import OrmBase


class Permiso(OrmBase.Base):
    __tablename__ = 'permiso'

    idPermiso = Column(Integer, primary_key=True)
    rfcContribuyente = Column(String(20))
    rfcRepresentanteLegal = Column(String(20))
    rfcProveedor = Column(String(20))
    caracter = Column(String(20))
    modalidadPermiso = Column(String(20))
    numPermiso = Column(String(20))
    numContratoOAsignacion = Column(String(30))
    instalacionAlmacenGasNatural = Column(String(260))
    claveInstalacion = Column(String(20))
    descripcionInstalacion = Column(String(260))
    latitud = Column(Float)
    longitud = Column(Float)
    nPozos = Column(Integer, default=0)
    nTanques = Column(Integer, default=0)
    nDuctosEntradaSalida = Column(Integer, default=0)
    nDuctosTransporteDistribucion = Column(Integer, default=0)
    nDispensarios = Column(Integer, default=0)
