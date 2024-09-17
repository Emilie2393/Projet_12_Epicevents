import os
from .permissions import check_permission, check_permission_update_contract, check_permission_event_creation

class MainController:

    def __init__(self, cli, contributors, contracts, clients, events):
        self.cli = cli
        self.contributors = contributors
        self.contracts = contracts
        self.clients = clients
        self.events = events

    def first_menu(self):
        choice = 0
        while choice != "1" or "2":
            choice = self.cli.main_menu()
            if choice == "1":
                data = self.cli.login_menu()
                check_login = self.contributors.login_user(data[0], data[1])
                if check_login:
                    self.login_menu()
                else:
                    print("Try again")
                    self.first_menu()
            if choice == "2":
                if self.contributors.first_user():
                    data = self.cli.register_menu()
                    self.contributors.register_user(data[0], data[1], data[2], data[3])
                else:
                    print("Please login to create a new user")
                
    def login_menu(self):
        choice = 0
        while choice != "1" or "2" or "3" or "4" or "5":
            choice = self.cli.summary_menu()
            check = self.contributors.verify_access_token(os.environ['SECRET_KEY'])
            if check:
                if choice == "1":
                    self.contract_menu()
                if choice == "2":
                    self.clients_menu()
                if choice == "3":
                    self.events_menu()
                if choice == "4":
                    if check_permission(check["sub"], "management"):
                        self.contributors_menu()
                    else:
                        print("You need to be in the management team to access this menu.")
                if choice == "5":
                    self.first_menu()
            else:
                print("Your connexion time is out, please login again")
                self.first_menu()
    
    def contributors_menu(self):
        choice = 0
        while choice != "1" or "2" or "3":
            choice = self.cli.contributors_menu()
            check = self.contributors.verify_access_token(os.environ['SECRET_KEY'])
            if check:
                if choice == "1":
                    data = self.cli.register_menu()
                    self.contributors.register_user(data[0], data[1], data[2], data[3])
                if choice == "2":
                    contributor_id = self.cli.object_id("user")
                    params = self.cli.user_params()
                    self.contributors.update_user(contributor_id, params[0], params[1])
                if choice == "3":
                    contributor_id = self.cli.object_id("user")
                    self.contributors.delete_user(contributor_id)
                self.login_menu()
            else:
                print("Your connexion time is out, please login again")
                self.first_menu()
    
    def clients_menu(self):
        choice = 0
        while choice != "1" or "2" or "3":
            choice = self.cli.clients_menu()
            check = self.contributors.verify_access_token(os.environ['SECRET_KEY'])
            if check:
                if choice == "1":
                    if check_permission(check["sub"], "commercial"):
                        client_info = self.cli.register_client()
                        self.clients.register_client(client_info[0], client_info[1], client_info[2], client_info[3], check["sub"])
                    else:
                        print("You are not allowed to do this")
                if choice == "2":
                    client_id = self.cli.object_id("client")
                    self.clients.get_client_info(client_id)
                if choice == "3":
                    client_id = self.cli.object_id("client")
                    params = self.cli.client_params()
                    self.clients.update_client(client_id, params[0], params[1], check["sub"])
                self.login_menu()
            else:
                print("Your connexion time is out, please login again")
                self.first_menu()
    
    def contract_menu(self):
        choice = 0
        while choice != "1" or "2" or "3" or "4":
            choice = self.cli.contracts_menu()
            check = self.contributors.verify_access_token(os.environ['SECRET_KEY'])
            if check:
                if choice == "1":
                    if check_permission(check["sub"], "management"):
                        contract_info = self.cli.register_contract()
                        self.contracts.register_contract(contract_info[0], contract_info[1],contract_info[2],contract_info[3])
                    else:
                        print("You are not allowed to do this")
                if choice == "2":
                    contract_id = self.cli.object_id("contract")
                    self.contracts.get_contract_info(contract_id)
                if choice == "3":
                    if check_permission(check["sub"], "commercial", "management"):
                        contract_id = self.cli.object_id("contract")
                        if check_permission_update_contract(check["sub"], contract_id):
                            params = self.cli.contract_params()
                            self.contracts.update_contract(contract_id, params[0], params[1])
                        else:
                            print("You are not allowed to update this contract.")
                    else:
                        print("You are not allowed to do this if you are in support team.")
                if choice == "4":
                    params = self.cli.data_filter()
                    self.contracts.get_contracts_filtered(params[0], params[1])
                self.login_menu()
            else:
                print("Your connexion time is out, please login again")
                self.first_menu()

    def events_menu(self):
        choice = 0
        while choice != "1" or "2" or "3" or "4":
            choice = self.cli.events_menu()
            check = self.contributors.verify_access_token(os.environ['SECRET_KEY'])
            if check:
                if choice == "1":
                    if check_permission(check["sub"], "commercial"):
                        event_info = self.cli.register_event()
                        if check_permission_event_creation(check["sub"], event_info[0]):
                            self.events.register_event(event_info[0], event_info[1], event_info[2], event_info[3], event_info[4], event_info[5])
                        else:
                            print("This contract isn't associated with your client.")
                if choice == "2":
                    object_id = self.cli.object_id("event")
                    self.events.get_event_info(object_id)
                if choice == "3":
                    if check_permission(check["sub"], "management", "support"):
                        object_id = self.cli.object_id("event")
                        params = self.cli.event_param()
                        self.contracts.update_event(object_id, params[0], params[1], check["sub"])
                    else:
                        print("You are not allowed to do this")
                if choice == "4":
                    params = self.cli.data_filter()
                    self.events.get_events_filtered(params[0], params[1])
                self.login_menu()

