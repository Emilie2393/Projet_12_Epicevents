from models.models import User, Contract, Client, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

def check_permission(mail, role, scd_role=""):
    user = session.query(User).filter_by(email=mail).first()
    if user.department == role:
        return True
    if scd_role:
        if user.department == scd_role:
            return True
    return False

def check_permission_update_client(mail, client_id):
    client = session.query(Client).filter(Client.id == client_id).first()
    user = session.query(User).filter_by(email=mail).first()
    if (user.id == client.commercial_id) or not client.commercial_id:
        return True
    return False

def check_permission_update_contract(mail, contract_id):
    contract = session.query(Contract).filter(Contract.id == contract_id).first()
    user = session.query(User).filter_by(email=mail).first()
    if (user.department == "commercial" and user.id == contract.commercial_id) or (user.department == "management"):
        return True
    return False

def check_permission_event_creation(mail, contract_id):
    contract = session.query(Contract).filter(Contract.id == contract_id).first()
    client = session.query(Client).filter(Client.id == contract.client_id).first()
    user = session.query(User).filter_by(email=mail).first()
    if ((client.commercial_id == user.id) and (contract.status == "signed")):
        return True
    return False 


