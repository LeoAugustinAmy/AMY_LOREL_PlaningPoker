import customtkinter as ctk

class HeaderView(ctk.CTkFrame):
    """!
    @brief Barre de navigation supérieure commune à l'application.
    """

    def __init__(self, parent, controller):
        """!
        @brief Initialise le Header.
        @param parent Widget parent.
        @param controller Contrôleur (MainController).
        """
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)

        ctk.CTkLabel(self, text="AMY LOREL — Planning Poker", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=12, pady=8)

        self.home_btn = ctk.CTkButton(self, text="Accueil", width=100, command=self._on_home)
        self.home_btn.grid(row=0, column=1, padx=6, pady=6)

        self.quit_btn = ctk.CTkButton(self, text="Quitter", width=80, fg_color="transparent", text_color="red", command=self._on_quit)
        self.quit_btn.grid(row=0, column=2, padx=12, pady=6)

    def _on_home(self):
        """!
        @brief Gestionnaire d'événement pour le bouton Accueil.
        """
        if self.controller:
            try:
                self.controller.show_home()
            except Exception:
                pass

    def _on_quit(self):
        """!
        @brief Gestionnaire d'événement pour le bouton Quitter.
        """
        if self.controller:
            try:
                self.controller.quit_app()
            except Exception:
                pass
        else:
            try:
                self.master.destroy()
            except Exception:
                pass