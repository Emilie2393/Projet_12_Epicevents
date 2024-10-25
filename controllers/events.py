from models.models import Contract, Client, User, get_next_id, session, Event
import datetime

class Events:

    def register_event(self, contract_id, start_date, end_date, location, attendees, notes):
        event_id = get_next_id(Event)
        contract = session.query(Contract).filter_by(id=contract_id).first()
        client = session.query(Client).filter_by(id=contract.client_id).first()
        client_name = client.name
        client_contact = client.email
        event_start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        event_end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        event = Event(id=event_id, contract_id=contract_id, client_name=client_name, client_contact=client_contact, 
                    event_start_date=event_start_date, event_end_date=event_end_date,
                    location=location, attendees=attendees, notes=notes)
        try:
            session.add(event)
            session.commit()
        except Exception as error:
            if "contract_id" in (str(error).split('\n')[0]):
                print("Wrong contract id, please try again")
            else:
                print(error)
            session.rollback()
    
    def get_event_info(self, id):
        event = session.query(Event).filter(Event.id == id).first()
        if event:
            support_contact = session.query(User).filter(User.id == event.support_contact_id).first()
            print(f'Contract id: {event.contract_id} \nClient name: {event.client_name} \nClient email: {event.client_contact} \
                \nEvent start date: {event.event_start_date} \nEvent end date: {event.event_end_date} \nSupport contact: {support_contact.name} \
                \nLocation: {event.location} \nAttendees number: {event.attendees} \nEvent notes: {event.notes} \n')
        else:
            print("This event doesn't exist. Please try again")
        
    def get_events_filtered(self, param, data):
        result = session.query(Event).filter(getattr(Event, param) == data).all()
        if result:
            for i in result:
                self.get_event_info(i.id)
        else:
            print("There is no parameter or data by this name")
    
    def update_event(self, id, param, new_param, user_email):
        # Updating events is possible only for the management team
        event = session.query(Event).filter(Event.id == id).first()
        user = session.query(User).filter(User.email == user_email).first()
        if event:
            if user.department == "managament":
                # Management team need to select a support team member for each event
                if param == "support_contact_id":
                    support = session.query(User).filter_by(id=new_param).first()
                    if support.department != "support":
                        print("This user is not from support department, please choose another one.")
                        return
                else:
                    print("You are not allowed to update something else than support_contact_id parameter.")
                    return
            try:
                setattr(event, param, new_param)
                session.commit()
            except Exception as error:
                print(error)
        else:
            print("This event doesn't exist.")

