from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import OrmBase


class Certificado(OrmBase.Base):
    __tablename__ = 'certificado'

    idPermiso = Column(Integer, ForeignKey(
        'permiso.idPermiso'), primary_key=True)
    idCertificado = Column(Integer, primary_key=True)
    rfcCertificado = Column(String(20))
    nFolioCertificado = Column(String(30))
    fechaEmisionCertificado = Column(Date)
    resultadoCertificado = Column(String(310))

    permiso = relationship("Permiso", backref="certificados")
