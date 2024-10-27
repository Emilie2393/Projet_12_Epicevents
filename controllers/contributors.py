from models.models import User, Client, Contract, Event, session, get_next_id
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
        # Create a new id following the previous one
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
        except Exception as error:
            if "email" in (str(error).split('\n')[0]):
                print("This email is wrong or has already been used in the database. Please try again.")
            elif "department" in (str(error).split('\n')[0]):
                print("The department must be commercial, management or support. Please try again.")
            else:
                print(error)
            session.rollback()

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
            print("Token has expired.")
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
                # The password updated need to be hached
                user.set_password(new_param)
                session.commit()
                print(f"{user.name}'s password has been correctly updated.")
                return
            try:
                # equivalent to user.param = new_param
                setattr(user, param, new_param)
                session.commit()
                print("This user has been correctly updated.")
                capture_message('This user has been correctly updated in the database.')
            except Exception as error:
                if "email" in (str(error).split('\n')[0]):
                    print("This email is wrong or is already used. Please try again.")
                elif "department" in (str(error).split('\n')[0]):
                    print("The department must be commercial, management or support. Please try again.")
                else:
                    print(error)
                session.rollback()
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
            print(f"Token is valid. User email is: {payload.get('sub')}")
            return True
        else:
            print("Invalid token.")

    def delete_user(self, user_id):
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            # First we delete the user id attached to client, contract and event tables
            client = session.query(Client).filter(getattr(Client, "commercial_id") == user.id).all()
            if client:
                for i in client:
                    i.commercial_id = None
                    print(f"You need to update the commercial for the client {i.name}")
            contract = session.query(Contract).filter(getattr(Contract, "commercial_id") == user.id).all()
            if contract:
                for e in contract:
                    e.commercial_id = None
                    print(f"You need to update the commercial for the contract {e.id}")
            event = session.query(Event).filter(getattr(Event, "support_contact_id") == user.id).all()
            if event:
                for f in event:
                    f.support_contact_id = None
                    print(f"You need to update the support contact for the event {f.id}")
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

