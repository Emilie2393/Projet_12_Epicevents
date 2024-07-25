from models.models import User, Contract, engine
from sqlalchemy import func, exists
from sqlalchemy.orm import sessionmaker
import datetime

Session = sessionmaker(bind=engine)
session = Session()

class Contracts:

    # def __init__(self, cli):
    #     self.cli = cli

    def get_next_contract_id(self):
        # Query to get the current maximum ID
        contract_id = session.query(exists().where(Contract.id != None)).scalar()
        if contract_id:
            max_id = session.query(func.max(Contract.id)).scalar()
        else:
            return 1
        
        # # If there are no users in the table, start with ID 1
        # if max_id is None:
        #     return 1
        
        # Increment the maximum ID to get the next ID
        return max_id + 1

    def register_contract(self, client_id, commercial, cost, due, status):
        
        contract_id = self.get_next_contract_id()
        client_details = "test"
        creation_date = datetime.date.today()
        print(creation_date)
        commercial = session.query(User).filter_by(id=commercial).first()
        commercial_name = commercial.name
        
        
        contract = Contract(id=contract_id, client_id=client_id, client_details=client_details, commercial=commercial_name, cost=cost, due=due, status=status, creation_date=creation_date)
        
        # Add and commit the new user to the database
        session.add(contract)
        session.commit()

