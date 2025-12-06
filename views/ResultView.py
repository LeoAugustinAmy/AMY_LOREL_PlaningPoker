import customtkinter as ctk

# --- Constantes de Design ---
THEME_HEADER_BG = ("gray85", "gray17")
THEME_COLOR_SUCCESS = "#2CC985"
THEME_COLOR_ACCENT = "#3B8ED0"

class ResultView(ctk.CTkFrame):
    """!
    @brief Vue affichant le bilan de la partie.
    @details Liste les User Stories estimées et permet de sauvegarder ou quitter.
    @attributes
        controller Contrôleur des résultats associé.
    """

    def __init__(self, parent, controller):
        """!
        @brief Constructeur de la ResultView.
        @param parent Conteneur parent (MainWindow).
        @param controller Contrôleur associé (ResultController).
        @return None
        @note Prépare la zone scrollable des résultats et le footer d'actions.
        """
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header_frame = ctk.CTkFrame(self, fg_color=THEME_HEADER_BG, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew", ipady=15)
        
        ctk.CTkLabel(self.header_frame, text="BILAN DE LA SESSION", 
                     font=("Roboto Medium", 24, "bold")).pack()
        ctk.CTkLabel(self.header_frame, text="Toutes les fonctionnalités ont été estimées.", 
                     font=("Arial", 14), text_color="gray").pack()

        self.results_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.results_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=20)

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
        @return None
        @example
            result_view.refresh_ui()
        """
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if self.controller:
            results = self.controller.get_results()
        else:
            results = {}

        if not results:
            ctk.CTkLabel(self.results_frame, text="Aucun résultat disponible.", font=("Arial", 16)).pack(pady=20)
            return

        for feature, score in results.items():
            self._create_result_row(feature, score)

    def _create_result_row(self, feature_name, score):
        """!
        @brief Crée une ligne visuelle pour un résultat.
        @param feature_name Nom de la fonctionnalité.
        @param score Score validé.
        @return None
        @note Convertit les cartes spéciales "cafe" et "interro" en symboles.
        """
        row = ctk.CTkFrame(self.results_frame, fg_color=("gray90", "gray20"), corner_radius=10)
        row.pack(fill="x", pady=5, ipadx=10, ipady=10)

        ctk.CTkLabel(row, text=str(feature_name), font=("Arial", 16), 
                     wraplength=500, justify="left").pack(side="left", padx=10)

        display_score = str(score)
        if score == "cafe": display_score = "☕"
        elif score == "interro": display_score = "?"

        badge = ctk.CTkFrame(row, fg_color=THEME_COLOR_SUCCESS, corner_radius=20, width=50, height=40)
        badge.pack(side="right", padx=10)
        badge.pack_propagate(False) 
        
        ctk.CTkLabel(badge, text=display_score, font=("Arial", 18, "bold"), text_color="white").pack(expand=True)

    def _on_save(self):
        """!
        @brief Déclenche la sauvegarde des résultats.
        @return None
        @note Délègue au contrôleur la création du fichier.
        """
        if self.controller: self.controller.save_results()

    def _on_home(self):
        """!
        @brief Retourne à l'accueil via le contrôleur.
        @return None
        @note N'effectue aucune action si aucun contrôleur n'est attaché.
        """
        if self.controller: self.controller.go_home()
