import customtkinter as ctk
from views.MainWindow import MainWindow
from controllers.MainController import MainController

# Configuration globale
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    app = MainWindow()
    controller = MainController(app)
    app.set_controller(controller)
    app.mainloop()