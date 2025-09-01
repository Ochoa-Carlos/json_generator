from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import OrmBase


class Archivo(OrmBase.Base):
    __tablename__ = 'archivo'

    idArchivo = Column(Integer, primary_key=True)
    idPermiso = Column(Integer, ForeignKey('permiso.idPermiso'))
    nombre = Column(String(250))
    estado = Column(Integer)
    comentarios = Column(Text)
    fecha = Column(DateTime)

    permiso = relationship("Permiso", backref="archivos")
