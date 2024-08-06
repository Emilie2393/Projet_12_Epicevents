from models.models import Client, User, session, get_next_id
import datetime


class Clients:
     

    def register_client(self, name, email, phone, company, commercial_id):
            # Check if the username already exists
            existing_client = session.query(Client).filter_by(email=email).first()
            if existing_client:
                print('Email adress already exists')
            
            client_id = get_next_id(Client)
            creation_date = datetime.date.today()
            commercial_id = session.query(User).filter_by(id=commercial_id).first()
            if not commercial_id:
                print("Your commercial ID is unknown")

            else:

                client = Client(id=client_id, name=name, email=email, phone=phone, company=company, creation_date=creation_date, commercial_id=commercial_id)
                
                # Add and commit the new client to the database
                session.add(client)
                session.commit()
                return True
    
    def get_client_info(self, id):
        client = session.query(Client).filter(Client.id == id).first()
        print(client)