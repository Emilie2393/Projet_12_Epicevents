from models.models import User, Contract, engine
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

def check_permission_update(mail, contract_id):
    contract = session.query(Contract).filter(Contract.id == contract_id).first()
    user = session.query(User).filter_by(email=mail).first()
    if (user.department == "commercial" and user.id == contract.commercial_id) or (user.department == "management"):
        return True
    return False
