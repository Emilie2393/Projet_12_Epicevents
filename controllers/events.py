from models.models import Contract, Client, User, get_next_id, session, Event
from sqlalchemy.exc import IntegrityError
import datetime

class Events:

    def register_event(self, contract_id, start_date, end_date, support_contact_id, location, attendees, notes):
        event_id = get_next_id(Event)
        contract = session.query(Contract).filter_by(id=contract_id).first()
        client = session.query(Client).filter_by(id=contract.client_id).first()
        client_name = client.name
        client_contact = client.email
        event_start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        event_end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        support_contact = session.query(User).filter_by(id=support_contact_id).first()
        if support_contact.department != "support":
            print("This user is not from support department, please choose another one.")
        else:
            event = Event(id=event_id, contract_id=contract_id, client_name=client_name, client_contact=client_contact, 
                        event_start_date=event_start_date, event_end_date=event_end_date, support_contact_id=support_contact_id, 
                        location=location, attendees=attendees, notes=notes)
            try:
                session.add(event)
                session.commit()
            except IntegrityError as e:
                if "support_contact_id" in IntegrityError:
                    print("Wrong support contact id, please try again")
                elif "contract_id" in IntegrityError:
                    print("Wrong contract id, please try again")
    
    def get_event_info(self, id):
        event = session.query(Event).filter(Event.id == id).first()
        support_contact = session.query(User).filter(User.id == event.support_contact_id).first()
        print(f'Contract id: {event.contract_id} \nClient name: {event.client_name} \nClient email: {event.client_contact} \
              \nEvent start date: {event.event_start_date} \nEvent end date: {event.event_end_date} \nSupport contact: {support_contact.name} \nLocation: \
                {event.location} \nAttendees number: {event.attendees} \nEvent notes: {event.notes}')

