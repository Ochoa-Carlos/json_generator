from sqlalchemy import Column, Integer, DateTime, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import OrmBase


class Bitacora(OrmBase.Base):
    __tablename__ = 'bitacora'

    idBitacora = Column(Integer, primary_key=True)
    idPermiso = Column(Integer, ForeignKey('permiso.idPermiso'))
    fechaYHoraEvento = Column(DateTime)
    tipoEvento = Column(Integer)
    descripcionEvento = Column(String(260))
    usuario = Column(String(100))
    evento = Column(Integer)

    permiso = relationship("Permiso", backref="bitacoras")
