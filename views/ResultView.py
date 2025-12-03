import customtkinter as ctk

# --- Constantes de Design ---
THEME_HEADER_BG = ("gray85", "gray17")
THEME_COLOR_SUCCESS = "#2CC985"
THEME_COLOR_ACCENT = "#3B8ED0"

class ResultView(ctk.CTkFrame):
    """!
    @brief Vue affichant le bilan de la partie.
    @details Liste les User Stories estimées et permet de sauvegarder ou quitter.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Layout principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. HEADER
        self.header_frame = ctk.CTkFrame(self, fg_color=THEME_HEADER_BG, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew", ipady=15)
        
        ctk.CTkLabel(self.header_frame, text="BILAN DE LA SESSION", 
                     font=("Roboto Medium", 24, "bold")).pack()
        ctk.CTkLabel(self.header_frame, text="Toutes les fonctionnalités ont été estimées.", 
                     font=("Arial", 14), text_color="gray").pack()

        # 2. LISTE DES RÉSULTATS (Scrollable)
        self.results_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.results_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=20)

        # 3. FOOTER (Boutons)
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.grid(row=2, column=0, sticky="ew", padx=40, pady=30)
        
        self.btn_save = ctk.CTkButton(self.footer_frame, text="💾 Enregistrer la Partie", 
                                      font=("Arial", 16, "bold"), height=50, width=200,
                                      fg_color=THEME_COLOR_ACCENT, hover_color="#2C6E9F",
                                      command=self._on_save)
        self.btn_save.pack(side="left")

        self.btn_home = ctk.CTkButton(self.footer_frame, text="Retour Accueil 🏠", 
                                      font=("Arial", 16, "bold"), height=50, width=200,
                                      fg_color="transparent", border_width=2, border_color="gray",
                                      hover_color=("gray90", "gray20"), text_color=("gray10", "gray90"),
                                      command=self._on_home)
        self.btn_home.pack(side="right")

    def refresh_ui(self):
        """!
        @brief Charge et affiche les résultats depuis le contrôleur.
        """
        # Nettoyage de la liste
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if self.controller:
            results = self.controller.get_results()
        else:
            results = {}

        if not results:
            ctk.CTkLabel(self.results_frame, text="Aucun résultat disponible.", font=("Arial", 16)).pack(pady=20)
            return

        # Affichage des lignes
        for feature, score in results.items():
            self._create_result_row(feature, score)

    def _create_result_row(self, feature_name, score):
        """!
        @brief Crée une ligne visuelle pour un résultat.
        """
        row = ctk.CTkFrame(self.results_frame, fg_color=("gray90", "gray20"), corner_radius=10)
        row.pack(fill="x", pady=5, ipadx=10, ipady=10)

        # Nom de la feature (gauche)
        ctk.CTkLabel(row, text=str(feature_name), font=("Arial", 16), 
                     wraplength=500, justify="left").pack(side="left", padx=10)

        # Badge de score (droite)
        display_score = str(score)
        if score == "cafe": display_score = "☕"
        elif score == "interro": display_score = "?"

        badge = ctk.CTkFrame(row, fg_color=THEME_COLOR_SUCCESS, corner_radius=20, width=50, height=40)
        badge.pack(side="right", padx=10)
        badge.pack_propagate(False) 
        
        ctk.CTkLabel(badge, text=display_score, font=("Arial", 18, "bold"), text_color="white").pack(expand=True)

    def _on_save(self):
        if self.controller:
            self.controller.save_results()

    def _on_home(self):
        if self.controller:
            self.controller.go_home()