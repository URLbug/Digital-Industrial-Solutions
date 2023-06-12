from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

from __init__ import config


DATABASE_NAME = 'Bot'

engine = create_engine(config['DATABASE'])

Base = declarative_base()
metadata_obj = MetaData()

Session = sessionmaker(bind=engine)

session = Session()

user = Table(
  "user",
  metadata_obj,
  Column("id", Integer, primary_key=True),
  Column("id_user", String(100)),
  Column("name_user", String(100)),
  Column("types", String(50)),
  Column("description", String(500))
)

reviews = Table(
  "reviews",
  metadata_obj,
  Column("id", Integer, primary_key=True),
  Column("id_user", String(100)),
  Column("name_user", String(100)),
  Column("reviews", String(500))
)


class User(Base):

  __tablename__ = 'user'

  id = Column(Integer, primary_key=True)
  id_user = Column(String(100))
  name_user = Column(String(100))
  types = Column(String(50))
  description = Column(String(500))
  
  def update_count_offers(id_to_update, new_desc):
    try:
        query = session.query(User).filter(User.id_user == id_to_update).\
            update({User.count_offers: new_desc}, synchronize_session=False)
        session.commit()
    except:
        session.rollback()

class Reviews(Base):

  __tablename__ = 'reviews'

  id = Column(Integer, primary_key=True)
  id_user = Column(String(100))
  name_user = Column(String(100))
  reviews = Column(String(500))
  
  def update_count_offers(id_to_update, new_desc):
    try:
        query = session.query(User).filter(Reviews.id_user == id_to_update).\
            update({User.count_offers: new_desc}, synchronize_session=False)
        session.commit()
    except:
        session.rollback()
    
class Admin(Base):

  __tablename__ = 'admin'

  id = Column(Integer, primary_key=True)
  id_user = Column(String(100))
  name_user = Column(String(100))
  
  def update_count_offers(id_to_update, new_desc):
    try:
        query = session.query(User).filter(Admin.id_user == id_to_update).\
            update({User.count_offers: new_desc}, synchronize_session=False)
        session.commit()
    except:
        session.rollback()


def creates(what):
  try:
    what.create(engine)
  except:
    pass

table = [user, reviews]

for i in table:
    creates(i)