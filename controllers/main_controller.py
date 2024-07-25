class MainController:

    def __init__(self, cli, contributors, contracts):
        self.cli = cli
        self.contributors = contributors
        self.contracts = contracts

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
            if choice == "1":
                self.contract_menu()
            if choice == "2":
                self.contributors.register_user()
    
    def contract_menu(self):
        choice = 0
        while choice != "1" or "2" or "3":
            choice = self.cli.contracts_menu()
            if choice == "1":
                contract_info = self.cli.register_contract()
                self.contracts.register_contract(contract_info[0], contract_info[1],contract_info[2],contract_info[3],contract_info[4])
                
