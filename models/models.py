from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, ForeignKeyConstraint
import pymysql
from passlib.hash import argon2

engine = create_engine('mysql+pymysql://admin:Bizerba23!@localhost/epicevents')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Role(Base):
    __tablename__ = 'roles'

    id = Column(String(15), primary_key=True)
    department = Column(String(15), nullable=False)

    def __repr__(self):
        return f'Role {self.department}'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    email = Column(String(30))
    department = Column(String(15))
    password = Column(String(170), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['department'], ['roles.id'], name='fk_users_department'),
    )


    def set_password(self, password):
        self.password = argon2.hash(password)

    def check_password(self, input):
        print(self.password)
        return argon2.verify(input, self.password)

    def __repr__(self):
        return f'User {self.name}'


Base.metadata.create_all(engine)
