from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,index=True)
    username = Column(String(50), unique=True)

class categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    cat_name = Column(String(50))

class sub_categories(Base):
    __tablename__ = 'sub_categories'

    id = Column(Integer, primary_key=True)
    cat_id = Column(Integer, ForeignKey("categories.id"))
    sub_cat_name = Column(String(50))

class transacrions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True,index=True)
    date = Column(String(50), unique=True)
    description = Column(String(50), unique = True)
    amount = Column(Integer)
    cat_id = Column(Integer, ForeignKey("categories.id"))
    subcat_id = Column(Integer,ForeignKey("sub_categories.id"))