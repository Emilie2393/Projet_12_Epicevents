class MainController:

    def __init__(self, cli, contributors):
        self.cli = cli
        self.contributors = contributors

    def first_menu(self):
        choice = 0
        while choice != "1" or "2":
            choice = self.cli.main_menu()
            if choice == "1":
                self.contributors.test()
            if choice == "2":
                self.contributors.test()
