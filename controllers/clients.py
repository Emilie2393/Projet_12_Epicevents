from models.models import Client, User, session, get_next_id
import datetime


class Clients:
     

    def register_client(self, name, email, phone, company, commercial_email):

        client_id = get_next_id(Client)
        creation_date = datetime.date.today()
        commercial = session.query(User).filter(User.email == commercial_email).first()
        client = Client(id=client_id, name=name, email=email, phone=phone, company=company, creation_date=creation_date, commercial_id=commercial.id)
        # Add and commit the new client to the database
        try:
            session.add(client)
            session.commit()
            print("Your client has been correctly uploaded.")
        except Exception as error:
            if "email" in (str(error).split('\n')[0]):
                print("This email has already been used in the database. Please try again.")
            elif "phone" in (str(error).split('\n')[0]):
                print("This phone number is not correct. Please try again.")
            else:
                print(error)
            session.rollback()
    
    def get_client_info(self, id):
        client = session.query(Client).filter(Client.id == id).first()
        commercial = session.query(User).filter(User.id == client.commercial_id).first()
        print(f'Client name {client.name} \nClient email {client.email} \nClient phone {client.phone} \nClient company {client.company} \nClient creation date {client.creation_date} \nClient update date {client.update_date} \nClient commercial {commercial.name}')

    def update_client(self, id, param, new_param, commercial_email):
        client = session.query(Client).filter(Client.id == id).first()
        commercial = session.query(User).filter(User.email == commercial_email).first()
        if client:
            # If the commercial id match the client's commercial id
            if int(client.commercial_id) == commercial.id:
                try:
                    setattr(client, param, new_param)
                    client.update_date = datetime.date.today()
                    session.commit()
                    print("This client has been updated.")
                except Exception as error:
                    if "email" in (str(error).split('\n')[0]):
                        print("This email has already been used in the database. Please try again.")
                    elif "phone" in (str(error).split('\n')[0]):
                        print("This phone number is not correct. Please try again.")
                    else:
                        print(error)
                    session.rollback()
            else:
                print("You're not allowed to update this client")
        else:
            print("This client doesn't exist")
    
