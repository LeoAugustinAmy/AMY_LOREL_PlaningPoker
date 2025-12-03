import customtkinter as ctk

class SetupView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="Configuration de la Partie", font=("Arial", 24)).pack(pady=20)