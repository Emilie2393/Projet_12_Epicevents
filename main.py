from cli.main_cli import Cli
from controllers.contributors import Contributors
from controllers.main_controller import MainController

def main():
    menu = Cli()
    contributors = Contributors(menu)
    main_controller = MainController(menu, contributors)
    main_controller.first_menu()


if __name__ == "__main__":
    main()