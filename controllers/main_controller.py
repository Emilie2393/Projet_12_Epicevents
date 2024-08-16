import os
from .permissions import check_permission

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
                data = self.cli.register_menu()
                register = self.contributors.register_user(data[0], data[1], data[2], data[3])
                if register:
                    self.first_menu()
                else:
                    print("Try again")
                
    def login_menu(self):
        choice = 0
        while choice != "1" or "2" or "3" or "4":
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


    
    def clients_menu(self):
        choice = 0
        while choice != "1" or "2" or "3":
            choice = self.cli.clients_menu()
            check = self.contributors.verify_access_token(os.environ['SECRET_KEY'])
            if check:
                if choice == "1":
                    if check_permission(check["sub"], "commercial"):
                        client_info = self.cli.register_client()
                        self.clients.register_client(client_info[0], client_info[1], client_info[2], client_info[3], client_info[4])
                    else:
                        print("You are not allowed to do this")
                if choice == "2":
                    client_id = self.cli.object_id("client")
                    self.clients.get_client_info(client_id)
                if choice == "3":
                    client_id = self.cli.object_id("client")
                    params = self.cli.client_params()
                    self.clients.update_client(client_id, params[0], params[1])

            else:
                print("Your connexion time is out, please login again")
                self.first_menu()
    
    def contract_menu(self):
        choice = 0
        while choice != "1" or "2" or "3":
            choice = self.cli.contracts_menu()
            check = self.contributors.verify_access_token(os.environ['SECRET_KEY'])
            if check:
                if choice == "1":
                    if check_permission(check["sub"], "commercial"):
                        contract_info = self.cli.register_contract()
                        self.contracts.register_contract(contract_info[0], contract_info[1],contract_info[2],contract_info[3],contract_info[4])
                    else:
                        print("You are not allowed to do this")
                if choice == "2":
                    contract_id = self.cli.object_id("contract")
                    self.contracts.get_contract_info(contract_id)
                if choice == "3":
                    contract_id = self.cli.object_id("contract")
                    params = self.cli.contract_param()
                    self.contracts.update_contract(contract_id, params[0], params[1])

            else:
                print("Your connexion time is out, please login again")
                self.first_menu()

    def events_menu(self):
        choice = 0
        while choice != "1" or "2" or "3":
            choice = self.cli.events_menu()
            check = self.contributors.verify_access_token(os.environ['SECRET_KEY'])
            if check:
                if choice == "1":
                    if check_permission(check["sub"], "commercial"):
                        event_info = self.cli.register_event()
                        self.events.register_event(event_info[0], event_info[1], event_info[2], event_info[3], event_info[4], event_info[5], event_info[6])
                if choice == "2":
                    object_id = self.cli.object_id("event")
                    self.events.get_event_info(object_id)
                if choice == "3":
                    object_id = self.cli.object_id("event")
                    params = self.cli.event_param()
                    self.contracts.update_event(object_id, params[0], params[1])

