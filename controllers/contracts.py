from models.models import Contract, Client, User, get_next_id, session
from sentry_sdk import capture_message
import datetime

class Contracts:


    def register_contract(self, client_id, cost, due, status):
        
        contract_id = get_next_id(Contract)
        creation_date = datetime.date.today()
        client = session.query(Client).filter_by(id=client_id).first()
        client_details = f'{client.name}, {client.phone}, {client.email}'
        if status not in ["signed", "payed", "to_complete"]:
            print("The status need to be 'signed', 'payed' or 'to_complete'")
            return
        contract = Contract(id=contract_id, client_id=client_id, client_details=client_details, commercial_id=client.commercial_id, cost=cost, due=due, status=status, creation_date=creation_date)
        
        # Add and commit the new user to the database
        try:
            session.add(contract)
            session.commit()
            print(f"Your contract {contract.id} has been correctly created.")
        except Exception as error:
            if "client_id" in (str(error).split('\n')[0]):
                print("Wrong client id, please try again")
            else:
                print(error)
    
    def get_contracts_filtered(self, param, data):
        # Contract are filtered by checking the data according to the selected parameter
        result = session.query(Contract).filter(getattr(Contract, param) == data).all()
        if result:
            for i in result:
                # Every matching contract are printed with the get_contract_info function
                self.get_contract_info(i.id)
        else:
            print("There is no parameter or data by this name")

    def get_contract_info(self, id):
        contract = session.query(Contract).filter(Contract.id == id).first()
        if contract:
            commercial = session.query(User).filter(User.id == contract.commercial_id).first()
            print(f'Client id {contract.client_id} \nClient details {contract.client_details} \nCommercial {commercial.name} \nCost {contract.cost} \nDue {contract.due} \nCreation date {contract.creation_date} \nStatus {contract.status}')
        else:
            print("This contract doesn't exist. Please try again.")

    def update_contract(self, id, param, new_param):
        contract = session.query(Contract).filter(Contract.id == id).first()
        if contract:
            try:
                # Status parameter need some checking
                if param == "status" and new_param not in ["signed", "payed", "to_complete"]:
                    print("The status need to be 'signed', 'payed' or 'to_complete'")
                    return
                if param == "commercial_id":
                    user = session.query(User).filter(User.id == new_param).first()
                    if user.department != "commercial":
                        print("Please select a commercial team member.")
                        return
                if new_param == "signed":
                    capture_message(f"The contract {contract.id} has been signed, congrats !")
                setattr(contract, param, new_param)
                session.commit()
            except Exception as error:
                if "client_id" in (str(error).split('\n')[0]):
                    print("Wrong client id, please try again")
                else:
                    print(error)
        else:
            print("This contract doesn't exist.")
    
