from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey, Integer
from sqlalchemy.ext.automap import automap_base


def _setup_db_reflection_base():

  engine = create_engine(r'mssql+pyodbc://(local)\SQLEXPRESS/ANSA?driver=SQL+Server+Native+Client+11.0') #, echo=True)
  # produce our own MetaData object
  metadata = MetaData()
  # we can reflect it ourselves from a database, using options  such as 'only' to limit what tables we look at...
  metadata.reflect(engine, only=['ClientRegistration'])# 'lk_gender'])
  
  metadata.create_all()



_setup_db_reflection_base()