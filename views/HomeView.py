import customtkinter as ctk

class HomeView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(self, text="Planning Poker", font=("Arial", 40, "bold")).grid(row=1, column=0, pady=20)

        ctk.CTkButton(self, text="Nouvelle Partie", width=200, height=50,
                      command=lambda: self.controller.show_setup()).grid(row=2, column=0, pady=10)
        
        ctk.CTkButton(self, text="Charger une Partie", width=200, height=50,
                      command=lambda: print("Charger une Partie")).grid(row=3, column=0, pady=10)

        ctk.CTkButton(self, text="Quitter", width=200, height=50, fg_color="red", hover_color="darkred",
                      command=lambda: self.controller.quit_app()).grid(row=4, column=0, pady=10)