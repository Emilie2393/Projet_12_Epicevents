from cli.main_cli import Cli
from controllers.contributors import Contributors
from controllers.contracts import Contracts
from controllers.main_controller import MainController
from controllers.clients import Clients
from controllers.events import Events

def main():
    menu = Cli()
    contributors = Contributors()
    contracts = Contracts()
    clients = Clients()
    events = Events()
    main_controller = MainController(menu, contributors, contracts, clients, events)
    main_controller.first_menu()


if __name__ == "__main__":
    main()