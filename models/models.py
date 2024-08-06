from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, ForeignKeyConstraint, Date, Float
from sqlalchemy import func, exists
import pymysql
from passlib.hash import argon2
import os
from dotenv import load_dotenv
load_dotenv()


ADMIN = os.environ['ADMIN']
engine = create_engine(f'mysql+pymysql://admin:{ADMIN}@localhost/epicevents')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

def get_next_id(object):
        # Query to get the current maximum ID
        contract_id = session.query(exists().where(object.id != None)).scalar()
        if contract_id:
            max_id = session.query(func.max(object.id)).scalar()
        else:
            return 1
        
        # Increment the maximum ID to get the next ID
        return max_id + 1

class Role(Base):
    __tablename__ = 'roles'

    id = Column(String(15), primary_key=True)
    department = Column(String(15), nullable=False)

    def __repr__(self):
        return f'Department {self.department}'


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
        return f'{self.name}'


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, nullable=False)
    client_details = Column(String(50))
    commercial_id = Column(Integer, ForeignKey('users.id'))
    cost = Column(Float(30))
    due = Column(Float(30))
    creation_date = Column(Date)
    status = Column(String(50))

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), primary_key=True)
    phone = Column(Integer)
    company = Column(String(50))
    creation_date = Column(Date)
    update_date = Column(Date)
    commercial_id = Column(String(50))

    def __repr__(self):
        return f'Client {self.name} \nEmail {self.email} \nPhone {self.phone} \nCompany {self.company} \nCreation date {self.creation_date} \nCommercial {self.commercial_id}'




Base.metadata.create_all(engine)
