from cli.main_cli import Cli
from controllers.contributors import Contributors
from controllers.contracts import Contracts
from controllers.main_controller import MainController

def main():
    menu = Cli()
    contributors = Contributors()
    contracts = Contracts()
    main_controller = MainController(menu, contributors, contracts)
    main_controller.first_menu()


if __name__ == "__main__":
    main()