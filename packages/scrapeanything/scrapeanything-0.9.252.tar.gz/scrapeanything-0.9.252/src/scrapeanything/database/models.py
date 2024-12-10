'''SQLAlchemy Data Models.'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Numeric, Integer, Text, String, Date, DateTime, Time, Boolean, Enum, Float
from sqlalchemy import Table
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.sql import func
from sqlalchemy import orm
from sqlalchemy.sql import text
import enum
from sqlalchemy import Index
from scrapeanything.utils.type_utils import TypeUtils
from sqlalchemy.orm import relationship


Base = declarative_base()

class Model(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now())

class View(Base):
    __abstract__ = True