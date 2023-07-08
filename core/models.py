import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BIGINT, NVARCHAR, TIMESTAMP, CHAR, LONGTEXT, INTEGER, JSON, BOOLEAN
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


# Session
class Session:
    def __init__(self):
        self.engine_url = os.getenv('DB_URL')
        self.engine = create_engine(self.engine_url, echo=False)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        self.session = self.Session()

    def get_db(self):
        return self.session


# Users Model
class User(Base):
    __tablename__ = 'users'

    id = Column(BIGINT, primary_key=True)
    name = Column(NVARCHAR(length=128), nullable=False)
    old_fraction = Column(INTEGER, nullable=False)
    fraction = Column(INTEGER, nullable=False)
    update_time = Column(TIMESTAMP, nullable=False)
    consecutive_sign_in = Column(INTEGER, nullable=True, default=0)
    last_sign_in = Column(TIMESTAMP, nullable=True)

    log_entries = relationship("Log", back_populates="user")


# Log Model
class Log(Base):
    __tablename__ = 'log'

    id = Column(NVARCHAR(length=128), primary_key=True)
    event_time = Column(TIMESTAMP, nullable=False)
    user_id = Column(BIGINT, ForeignKey('users.id'), nullable=False)
    event = Column(NVARCHAR(length=128), nullable=False)

    user = relationship("User", back_populates="log_entries")

