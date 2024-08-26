from models.models import Contract, Client, User, get_next_id, session
from sqlalchemy.exc import IntegrityError
import datetime

class Contracts:


    def register_contract(self, client_id, cost, due, status):
        
        contract_id = get_next_id(Contract)
        creation_date = datetime.date.today()
        client = session.query(Client).filter_by(id=client_id).first()
        client_details = f'{client.name}, {client.phone}, {client.email}'
        contract = Contract(id=contract_id, client_id=client_id, client_details=client_details, commercial_id=client.commercial_id, cost=cost, due=due, status=status, creation_date=creation_date)
        
        # Add and commit the new user to the database
        try:
            session.add(contract)
            session.commit()
        except IntegrityError as e:
            if "commercial_id" in IntegrityError:
                print("Wrong commercial id, please try again")
            elif "client_id" in IntegrityError:
                print("Wrong client id, please try again")

    def get_contract_info(self, id):
        contract = session.query(Contract).filter(Contract.id == id).first()
        commercial = session.query(User).filter(User.id == contract.commercial_id).first()
        print(f'Client id {contract.client_id} \nClient details {contract.client_details} \nCommercial {commercial.name} \nCost {contract.cost} \nDue {contract.due} \nCreation date {contract.creation_date} \nStatus {contract.status}')

    def update_contract(self, id, param, new_param, user_email):
        contract = session.query(Contract).filter(Contract.id == id).first()
        if contract:
            try:
                setattr(contract, param, new_param)
                session.commit()
            except Exception as error:
                print(error)
        else:
            print("You can't update this contract")
