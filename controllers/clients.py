from models.models import Client, User, session, get_next_id
import datetime


class Clients:
     

    def register_client(self, name, email, phone, company, commercial_id):

            client_id = get_next_id(Client)
            creation_date = datetime.date.today()
            client = Client(id=client_id, name=name, email=email, phone=phone, company=company, creation_date=creation_date, commercial_id=commercial_id)
            
            # Add and commit the new client to the database
            session.add(client)
            session.commit()
            return True
    
    def get_client_info(self, id):
        client = session.query(Client).filter(Client.id == id).first()
        commercial = session.query(User).filter(User.id == client.commercial_id).first()
        print(f'Client name {client.name} \nClient email {client.email} \nClient phone {client.phone} \nClient company {client.company} \nClient creation date {client.creation_date} \nClient update date {client.update_date} \nClient commercial {commercial}')

    def update_client(self, id, param, new_param):
        client = session.query(Client).filter(Client.id == id).first()
        if client:
            if param == 'name':
                client.name = new_param
            elif param == 'email':
                client.email = new_param
            elif param == 'phone':
                client.phone = new_param
            elif param == 'company':
                client.company = new_param
            elif param == 'commercial_id':
                commercial = session.query(User).filter(User.id == id).first()
                client.commercial_id = commercial
            client.update_date = datetime.date.today()
            session.commit()
