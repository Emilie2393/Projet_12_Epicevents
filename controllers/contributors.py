from models.models import User, session, get_next_id
from sqlalchemy import func
import jwt
import os
import datetime
from dotenv import load_dotenv
load_dotenv()


class Contributors:

    def __init__(self):
        self.token = 0
    

    def register_user(self, name, password, email, department):
        # Check if the username already exists
        existing_user = session.query(User).filter_by(name=name).first()
        if existing_user:
            print('Username already exists')
        
        user_id = get_next_id(User)

        if department not in ["commercial", "management", "support"]:
            print("Your department must be commercial, management or support")

        else:

            user = User(id=user_id, name=name, email=email, department=department)
            # Hash the password and create a new user
            user.set_password(password)
            
            # Add and commit the new user to the database
            session.add(user)
            session.commit()
            return True
        
        return 'User registered successfully'


    def create_access_token(self, data, SECRET_KEY):
        expire = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=5)
        to_encode = {"sub": data, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
        self.token = encoded_jwt
        return encoded_jwt

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

    def login_user(self, email: str, password: str):
        user = self.authenticate_user(email, password)
        if not user:
            return None
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

