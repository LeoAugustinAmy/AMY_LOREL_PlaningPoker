import customtkinter as ctk

class CustomPopup(ctk.CTkToplevel):
    """!
    @brief Fenêtre contextuelle personnalisée (Popup) respectant le thème de l'application.
    @details Remplace les messagebox natifs de tkinter pour afficher des erreurs, avertissements ou succès.
    """

    def __init__(self, title, message, type="info", width=400, height=200):
        """!
        @brief Initialise et affiche la popup.
        @param title Le titre de la fenêtre.
        @param message Le message à afficher à l'utilisateur.
        @param type Type de message ("info", "error", "warning") influençant la couleur du bouton.
        @param width Largeur de la fenêtre (défaut 400).
        @param height Hauteur de la fenêtre (défaut 200).
        """
        super().__init__()

        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        
        # On force la fenêtre à être au premier plan
        self.attributes("-topmost", True)
        
        self._center_window(width, height)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        icons = {"info": "ℹ️", "error": "❌", "warning": "⚠️"}
        icon = icons.get(type, "ℹ️")
        
        self.label = ctk.CTkLabel(self, text=f"{icon}\n\n{message}", 
                                  font=("Roboto Medium", 14), wraplength=350)
        self.label.grid(row=0, column=0, padx=20, pady=20)

        colors = {"info": "#3B8ED0", "error": "#E04F5F", "warning": "#E5A00D"}
        btn_color = colors.get(type, "#3B8ED0")

        self.btn_ok = ctk.CTkButton(self, text="OK", width=100, height=35,
                                    fg_color=btn_color, hover_color=self._darken_color(btn_color),
                                    command=self.destroy)
        self.btn_ok.grid(row=1, column=0, pady=(0, 20))

        # Rendre la fenêtre modale (bloque les autres fenêtres)
        self.grab_set()

    def _center_window(self, width, height):
        """!
        @brief Calcule la position pour centrer la fenêtre sur l'écran.
        """
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _darken_color(self, hex_color, factor=0.8):
        """!
        @brief Assombrit une couleur hexadécimale pour l'effet de survol (hover).
        @return La couleur assombrie en hex.
        """
        return hex_color