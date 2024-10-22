from models.models import User, session, get_next_id
from sqlalchemy.exc import IntegrityError
from sentry_sdk import capture_message
import jwt
import os
import datetime
from dotenv import load_dotenv
load_dotenv()


class Contributors:

    def __init__(self):
        self.token = 0
    

    def register_user(self, name, email, password, department):
        # Check if the username already exists
        existing_user = session.query(User).filter_by(email=email).first()
        if existing_user:
            print('User email already exists')
        
        user_id = get_next_id(User)
        user = User(id=user_id, name=name, email=email, department=department)
        # Hash the password and create a new user
        user.set_password(password)
        
        # Add and commit the new user to the database
        try:
            session.add(user)
            session.commit()
            print(f'User {name} correctly created in the database.')
            capture_message(f'User {name} correctly created in the database.')
        except IntegrityError as e:
            if "department" in str(e):
                print('This department is wrong, please select commercial, support or management')

    def create_access_token(self, data, SECRET_KEY):
        # Set the expiration to 5 min
        expire = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=5)
        # User email and expiration time to set the jwt token
        to_encode = {"sub": data, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
        self.token = encoded_jwt

    def verify_access_token(self, SECRET_KEY):
        try:
            payload = jwt.decode(self.token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            # Signature has expired
            print("expired")
            return False

    def authenticate_user(self, email: str, password: str):
        user = session.query(User).filter(User.email == email).first()
        if not user:
            return False
        if not user.check_password(password):
            return False
        return user
    
    def update_user(self, id, param, new_param):
        user = session.query(User).filter(User.id == id).first()
        if user:
            if param == "password":
                user.set_password(new_param)
                session.commit()
                print(f"{user.name}'s password has been correctly updated.")
                return
            try:
                setattr(user, param, new_param)
                session.commit()
                print("This user has been correctly updated.")
                capture_message('This user has been correctly updated in the database.')
            except IntegrityError as e:
                if "department" in str(e):
                    print('This department is wrong, please select commercial, support or management')
        else:
            print("You can't update this user, it doesn't exist.")

    def login_user(self, email: str, password: str):
        # Check the users table from the database
        user = self.authenticate_user(email, password)
        if not user:
            return None
        # The secret key is set in .env file
        SECRET_KEY = os.environ['SECRET_KEY']
        self.create_access_token(data=user.email, SECRET_KEY=SECRET_KEY)
        if self.token:
            print(f"Access token: {self.token}")
        else:
            print("Login failed.")
        payload = self.verify_access_token(SECRET_KEY=SECRET_KEY)
        if payload:
            print(f"Token is valid. Username: {payload.get('sub')}")
            return True
        else:
            print("Invalid token.")
    
    def delete_user(self, user_id):
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            session.delete(user)
            session.commit()
            print("This contributor is now deleted")
        else:
            print("This user doesn't exist")

    def first_user(self):
        table = session.query(User).first()
        if table:
            return False
        else:
            return True


