import customtkinter as ctk

class SetupView(ctk.CTkFrame):
    """!
    @brief Vue de configuration de la partie.
    @details Permet d'ajouter des joueurs, des tâches, de choisir les règles et d'importer/exporter en JSON.
    """

    def __init__(self, parent, controller):
        """!
        @brief Constructeur de SetupView.
        @param parent Le widget parent (MainWindow).
        @param controller Le contrôleur associé (SetupController).
        """
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=1, uniform="group1")
        self.grid_rowconfigure(1, weight=1)

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(20, 10), padx=20)
        
        ctk.CTkLabel(self.header_frame, text="Configuration de la Session", 
                     font=("Roboto Medium", 24)).pack(side="left")

        self.btn_export = ctk.CTkButton(self.header_frame, text="Sauvegarder (JSON)", width=120, 
                                        fg_color="transparent", border_width=1, border_color="gray", text_color=("gray10", "gray90"),
                                        command=self.export_json)
        self.btn_export.pack(side="right", padx=5)
        
        self.btn_import = ctk.CTkButton(self.header_frame, text="Charger (JSON)", width=120, 
                                        fg_color="transparent", border_width=1, border_color="gray", text_color=("gray10", "gray90"),
                                        command=self.import_json)
        self.btn_import.pack(side="right", padx=5)

        self.left_card = ctk.CTkFrame(self, corner_radius=15)
        self.left_card.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=10)
        
        ctk.CTkLabel(self.left_card, text="📝 Saisie des données", font=("Roboto Medium", 18), text_color="gray70").pack(anchor="w", padx=20, pady=(20, 10))

        self.frame_add_player = ctk.CTkFrame(self.left_card, fg_color="transparent")
        self.frame_add_player.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(self.frame_add_player, text="Nouveau Joueur", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 5))
        
        self.entry_player = ctk.CTkEntry(self.frame_add_player, placeholder_text="Ex: Alice", height=40)
        self.entry_player.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_player.bind("<Return>", lambda event: self.add_player())
        
        self.btn_add_player = ctk.CTkButton(self.frame_add_player, text="+", width=40, height=40, 
                                            fg_color="#2CC985", hover_color="#229A65",
                                            command=self.add_player)
        self.btn_add_player.pack(side="right")

        ctk.CTkProgressBar(self.left_card, height=2, progress_color="gray30").pack(fill="x", padx=40, pady=20)

        self.frame_add_feat = ctk.CTkFrame(self.left_card, fg_color="transparent")
        self.frame_add_feat.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(self.frame_add_feat, text="Nouvelle Fonctionnalité (User Story)", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 5))
        
        self.entry_feature = ctk.CTkEntry(self.frame_add_feat, placeholder_text="Ex: Page de Login", height=40)
        self.entry_feature.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_feature.bind("<Return>", lambda event: self.add_feature())
        
        self.btn_add_feature = ctk.CTkButton(self.frame_add_feat, text="+", width=40, height=40, 
                                             fg_color="#3B8ED0", hover_color="#2C6E9F",
                                             command=self.add_feature)
        self.btn_add_feature.pack(side="right")

        self.right_card = ctk.CTkFrame(self, corner_radius=15)
        self.right_card.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=10)

        self.right_card.grid_rowconfigure(1, weight=1)
        self.right_card.grid_rowconfigure(3, weight=1)
        self.right_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.right_card, text="👥 Joueurs Inscrits", font=("Roboto Medium", 16)).grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))
        
        self.list_players = ctk.CTkScrollableFrame(self.right_card, fg_color="transparent")
        self.list_players.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        ctk.CTkLabel(self.right_card, text="📋 Backlog", font=("Roboto Medium", 16)).grid(row=2, column=0, sticky="w", padx=20, pady=(15, 5))
        
        self.list_features = ctk.CTkScrollableFrame(self.right_card, fg_color="transparent")
        self.list_features.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=20)

        self.rule_frame = ctk.CTkFrame(self.footer_frame, fg_color="transparent")
        self.rule_frame.pack(side="left")
        ctk.CTkLabel(self.rule_frame, text="Mode de validation :", font=("Arial", 14)).pack(side="left", padx=(0, 10))
        
        self.rules_var = ctk.StringVar(value="Unanimité")
        self.rules_menu = ctk.CTkOptionMenu(self.rule_frame, variable=self.rules_var, 
                                            values=["Unanimité"], width=200, dynamic_resizing=False)
        self.rules_menu.pack(side="left")

        self.btn_start = ctk.CTkButton(self.footer_frame, text="LANCER LA PARTIE 🚀", 
                                       font=("Arial", 16, "bold"), height=50, width=250,
                                       fg_color="#E04F5F", hover_color="#B03E4A",
                                       command=self.start_game)
        self.btn_start.pack(side="right")

    def add_player(self):
        """!
        @brief Action d'ajout d'un joueur déclenchée par l'interface.
        """
        if self.controller.add_player(self.entry_player.get().strip()):
            self.entry_player.delete(0, "end")
            self.refresh_lists()

    def add_feature(self):
        """!
        @brief Action d'ajout d'une fonctionnalité déclenchée par l'interface.
        """
        if self.controller.add_feature(self.entry_feature.get().strip()):
            self.entry_feature.delete(0, "end")
            self.refresh_lists()

    def import_json(self):
        """!
        @brief Déclenche l'importation de données JSON via le contrôleur.
        """
        if self.controller.import_data():
            self.refresh_lists()

    def export_json(self):
        """!
        @brief Déclenche l'exportation des données en JSON via le contrôleur.
        """
        self.controller.export_data()

    def start_game(self):
        """!
        @brief Valide la règle sélectionnée et demande au contrôleur de lancer le jeu.
        """
        self.controller.set_rule(self.rules_var.get())
        self.controller.start_game()

    def refresh_ui(self):
        """!
        @brief Met à jour l'ensemble de l'interface (règles et listes).
        @details Méthode appelée par le MainController lors de l'affichage de la vue.
        """
        rules = self.controller.get_available_rules()
        self.rules_menu.configure(values=rules)
        self.rules_var.set(rules[0])
        self.refresh_lists()

    def refresh_lists(self):
        """!
        @brief Reconstruit visuellement les listes de joueurs et de fonctionnalités.
        """
        for widget in self.list_players.winfo_children():
            widget.destroy()
        
        for p_name in self.controller.get_players():
            self._create_list_item(self.list_players, p_name, 
                                   lambda n=p_name: self.remove_player_ui(n), icon="👤")

        for widget in self.list_features.winfo_children():
            widget.destroy()

        for f_name in self.controller.get_features():
            self._create_list_item(self.list_features, f_name, 
                                   lambda n=f_name: self.remove_feature_ui(n), icon="📌")

    def _create_list_item(self, parent_frame, text, delete_command, icon=""):
        """!
        @brief Crée un élément de liste stylisé avec un bouton de suppression.
        @param parent_frame Le conteneur parent.
        @param text Le texte à afficher.
        @param delete_command La fonction à appeler lors du clic sur la suppression.
        @param icon Une icône textuelle optionnelle.
        """
        item_card = ctk.CTkFrame(parent_frame, fg_color=("gray85", "gray25"))
        item_card.pack(fill="x", pady=2, padx=2)
        
        full_text = f"{icon}  {text}" if icon else text
        ctk.CTkLabel(item_card, text=full_text, anchor="w").pack(side="left", padx=10, pady=5)
        
        btn_del = ctk.CTkButton(item_card, text="✕", width=30, height=30, 
                                fg_color="transparent", text_color="red", hover_color=("gray70", "gray30"),
                                command=delete_command)
        btn_del.pack(side="right", padx=5)

    def remove_player_ui(self, name):
        """!
        @brief Demande la suppression d'un joueur et rafraîchit l'interface.
        @param name Nom du joueur.
        """
        self.controller.remove_player(name)
        self.refresh_lists()

    def remove_feature_ui(self, name):
        """!
        @brief Demande la suppression d'une fonctionnalité et rafraîchit l'interface.
        @param name Nom de la fonctionnalité.
        """
        self.controller.remove_feature(name)
        self.refresh_lists()