from models.models import User, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

def check_permission(mail, role):
    user = session.query(User).filter_by(email=mail).first()
    if user.department == role:
        return True
    return False
