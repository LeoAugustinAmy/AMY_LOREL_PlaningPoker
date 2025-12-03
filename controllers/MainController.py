class MainController:
    def __init__(self, view):
        self.view = view

    def show_home(self):
        self.view.show_frame("HomeView")

    def show_setup(self):
        self.view.show_frame("SetupView")

    def quit_app(self):
        self.view.quit_app()