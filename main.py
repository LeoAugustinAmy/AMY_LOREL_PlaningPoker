import customtkinter as ctk
from views.MainWindow import MainWindow
from controllers.MainController import MainController

"""!
@brief Point d'entrée de l'application Planning Poker.
@details Configure le thème global, instancie la fenêtre principale et le contrôleur, puis lance la boucle événementielle.
"""

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    app = MainWindow()
    controller = MainController(app)
    app.set_controller(controller)
    app.mainloop()