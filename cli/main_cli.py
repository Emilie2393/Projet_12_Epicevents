class Cli:

    @staticmethod
    def main_menu():
        choice = input("Press the number associated to login or register to access EpicEvents please : \n"
                       "1 - Login \n"
                       "2 - Register \n")
        return choice
    
    @staticmethod
    def summary_menu():
        choice = input("Press the number associated to your choice : \n"
                       "1 - Contracts \n"
                       "2 - Clients \n"
                       "3 - Events \n"
                       "4 - CRM Users \n")
        return choice
    
    @staticmethod
    def contracts_menu():
        choice = input("Press the number associated to your choice : \n"
                       "1 - Register a new contract \n"
                       "2 - Get a contract informations \n"
                       "3 - Update a contract \n")
        return choice
    
    @staticmethod
    def contract_id():
        choice = input("Please enter the id of the contract you need to check : \n")
        return choice
    
    @staticmethod
    def register_contract():
        client_id = input("Enter client id: ")
        commercial = input("Enter commercial id: ")
        cost = input("Enter contract's cost: ")
        due = input("Enter contract's due: ")
        status = input("Enter contract's status: ")
        return client_id, commercial, cost, due, status
    
    @staticmethod
    def register_user():
        client_id = input("Enter client id: ")
        commercial = input("Enter commercial id: ")
        cost = input("Enter contract's cost: ")
        due = input("Enter contract's due: ")
        status = input("Enter contract's status: ")
        return client_id, commercial, cost, due, status
    
    @staticmethod
    def login_menu():
        email = input("Enter your email adress please: ")
        password = input("Enter your password please: ")
        return email, password
    
    @staticmethod
    def register_menu():
        name = input("Enter your name: ")
        email = input("Enter your email adress please: ")
        password = input("Enter your password please: ")
        department = input("Enter your department name: ")
        return name, email, password, department