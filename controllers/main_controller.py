import os
from .permissions import check_permission

class MainController:

    def __init__(self, cli, contributors, contracts, clients):
        self.cli = cli
        self.contributors = contributors
        self.contracts = contracts
        self.clients = clients
            

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
                    self.login_menu()
                if choice == "4":
                    self.login_menu()
                if choice == "5":
                    self.first_menu()
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
                        self.clients.register_client(client_info[0], client_info[1], client_info[2], client_info[3], client_info[4])
                    else:
                        print("You are not allowed to do this")
                if choice == "2":
                    client_id = self.cli.object_id("client")
                    self.clients.get_client_info(client_id)

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

            else:
                print("Your connexion time is out, please login again")
                self.first_menu()

                
