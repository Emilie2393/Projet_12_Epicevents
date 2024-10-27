from models.models import User, Contract, Client, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

def check_permission(mail, role, scd_role=""):
    # Check permission with the role of the user. Sometimes, 2 roles are allowed so there is the second role
    user = session.query(User).filter_by(email=mail).first()
    if user.department == role:
        return True
    if scd_role:
        if user.department == scd_role:
            return True
    return False

def check_permission_update_client(mail, client_id):
    # Check the permission for the user to update his client by matching their IDs
    client = session.query(Client).filter(Client.id == client_id).first()
    user = session.query(User).filter_by(email=mail).first()
    if (user.id == client.commercial_id) or not client.commercial_id:
        return True
    return False

def check_permission_update_contract(mail, contract_id):
    # Check the permission for the user to update his contract by matching their IDs and checking the user's role
    contract = session.query(Contract).filter(Contract.id == contract_id).first()
    user = session.query(User).filter_by(email=mail).first()
    if (user.department == "commercial" and user.id == contract.commercial_id) or (user.department == "management"):
        return True
    return False

def check_permission_event_creation(mail, contract_id):
    # Check the permission for the user to create an event once the contract associated has been signed and matching their IDs
    contract = session.query(Contract).filter(Contract.id == contract_id).first()
    client = session.query(Client).filter(Client.id == contract.client_id).first()
    user = session.query(User).filter_by(email=mail).first()
    if ((client.commercial_id == user.id) and (contract.status == "signed")):
        return True
    return False 


