from models import User, Role, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import jwt
from jwt import PyJWTError
import datetime

Session = sessionmaker(bind=engine)
session = Session()

# user = User(id=4, name="Anna", email="test@test.fr", department="commercial")
# user.set_password('coucou')
# print(len(user.password))
# session.add(user)
# session.commit()
# print(user.department)
# # u = session.query(User).get(3)
# print(u.password)
# print(u.check_password('coucou'))
# print(u.check_password('notherightpassword'))

# role1 = Role(id="management", department="management")
# role2 = Role(id="commercial", department="commercial")
# role3 = Role(id="support", department="support")
# session.add(role1)
# session.add(role2)
# session.add(role3)
# session.commit()

def get_next_user_id():
    # Query to get the current maximum ID
    max_id = session.query(func.max(User.id)).scalar()
    
    # If there are no users in the table, start with ID 1
    if max_id is None:
        return 1
    
    # Increment the maximum ID to get the next ID
    return max_id + 1

def register_user(name, password, email, department):
    # Check if the username already exists
    existing_user = session.query(User).filter_by(name=name).first()
    if existing_user:
        return 'Username already exists'
    
    user_id = get_next_user_id()
    
    user = User(id=user_id, name=name, email=email, department=department)
    # Hash the password and create a new user
    user.set_password(password)
    
    # Add and commit the new user to the database
    session.add(user)
    session.commit()
    
    return 'User registered successfully'

name = input("Entrez votre nom: ")
password = input("Entrez votre mot de passe: ")
email = input("Entrez votre email: ")
department = input("Entrez votre departement: ")

register_user(name, password, email, department)

SECRET_KEY = 'your_secret_key'

def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now() + expires_delta
    else:
        expire = datetime.datetime.now() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except PyJWTError:
        return None

def authenticate_user(email: str, password: str):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not user.check_password(password):
        return False
    return user

def login_user(email: str, password: str):
    user = authenticate_user(email, password)
    if not user:
        return None
    access_token = create_access_token(data={"sub": user.email})
    return access_token

email = input("email: ")
password = input("mot de passe: ")

token = login_user(email, password)
if token:
    print(f"Access token: {token}")
else:
    print("Login failed.")

payload = verify_access_token(token)
if payload:
    print(f"Token is valid. Username: {payload.get('sub')}")
else:
    print("Invalid token.")
