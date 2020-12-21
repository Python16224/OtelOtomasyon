from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class GirisCikis(Base):
    __tablename__ = 'giris_cikis'
    id = Column(Integer, primary_key=True)
    giris_tarihi = Column(String)
    cikis_tarihi = Column(String)
    fiyat = Column(String)
    oda_no = Column(String)


class MusteriListesi(Base):
    __tablename__ = 'musteri_listesi'
    id = Column(Integer, primary_key=True)
    musteri_id = Column(Integer, ForeignKey('giris_cikis.id'))
    tc_no = Column(String)
    adi = Column(String)
    soyadi = Column(String)
    oda_no = relationship('GirisCikis', backref=backref('musteri_listesi'))

