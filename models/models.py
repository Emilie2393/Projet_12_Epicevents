from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, validates
import re
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, ForeignKeyConstraint, Date, Float
from sqlalchemy import func, exists
import pymysql
import sentry_sdk
from passlib.hash import argon2
import os
from dotenv import load_dotenv
load_dotenv()

sentry_sdk.init(
    dsn="https://1471a7a48d46de5000fb0c6472585de4@o4507968058687488.ingest.de.sentry.io/4507968131366992",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

ADMIN = os.environ['ADMIN']
engine = create_engine(f'mysql+pymysql://admin:{ADMIN}@localhost/epicevents')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

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
    email = Column(String(30), nullable=False, unique=True)
    department = Column(String(15))
    password = Column(String(170), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['department'], ['roles.id'], name='fk_users_department'),
    )

    @validates('email')
    def validate_email(self, key, email):
        """Custom validator to check if email is in correct format."""
        if not re.match(EMAIL_REGEX, email):
            raise ValueError(f"Invalid email format: {email}")
        return email

    def set_password(self, password):
        self.password = argon2.hash(password)

    def check_password(self, input):
        print(self.password)
        return argon2.verify(input, self.password)


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(Integer)
    company = Column(String(50))
    creation_date = Column(Date)
    update_date = Column(Date)
    commercial_id = Column(ForeignKey('users.id'))

    @validates('email')
    def validate_email(self, key, email):
        """Custom validator to check if email is in correct format."""
        if not re.match(EMAIL_REGEX, email):
            raise ValueError(f"Invalid email format: {email}")
        return email


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey('clients.id'))
    client_details = Column(String(50))
    commercial_id = Column(ForeignKey('users.id'))
    cost = Column(Float(30))
    due = Column(Float(30))
    creation_date = Column(Date)
    status = Column(String(50))


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    contract_id = Column(ForeignKey('contracts.id'))
    client_name = Column(String(50))
    client_contact = Column(String(50))
    event_start_date = Column(Date)
    event_end_date = Column(Date)
    support_contact_id = Column(ForeignKey('users.id'))
    location = Column(String(50))
    attendees = Column(Integer)
    notes = Column(String(200))


Base.metadata.create_all(engine)
roles = session.query(exists().where(Role.id != None)).scalar()

if not roles:
    commercial = Role(id='commercial', department='commercial')
    management = Role(id='management', department='management')
    support = Role(id='support', department='support')
    session.add(commercial)
    session.add(management)
    session.add(support)
    session.commit()
    print("Roles table has been created, you can now create a new contributor to begin.")

