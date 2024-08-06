from models.models import User, Contract, engine, get_next_id, session
from sqlalchemy import func, exists
from sqlalchemy.orm import sessionmaker
import datetime

class Contracts:


    def register_contract(self, client_id, commercial, cost, due, status):
        
        contract_id = get_next_id(Contract)
        client_details = "test"
        creation_date = datetime.date.today()
        print(creation_date)
        commercial = session.query(User).filter_by(id=commercial).first()
        commercial_name = commercial.name
        
        
        contract = Contract(id=contract_id, client_id=client_id, client_details=client_details, commercial=commercial_name, cost=cost, due=due, status=status, creation_date=creation_date)
        
        # Add and commit the new user to the database
        session.add(contract)
        session.commit()
    
    def get_contract_info(self, id):
        contract = session.query(Contract).filter(Contract.id == id).first()
        print(contract.client_details)

