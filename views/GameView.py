import customtkinter as ctk
from PIL import Image
import io
import os

# --- Configuration Cairosvg ---
try:
    import cairosvg
    CAIROSVG_AVAILABLE = True
except ImportError:
    CAIROSVG_AVAILABLE = False
    print("Info UI: cairosvg non détecté. Mode fallback texte activé.")

# --- Constantes de Design ---
CARD_SIZE_DECK = (70, 105)   # Taille des cartes dans la main
CARD_SIZE_TABLE = (80, 120)  # Taille des cartes révélées sur la table
PLAYER_SLOT_WIDTH = 120      # Largeur fixe pour aligner chaque joueur
THEME_COLOR_ACCENT = "#3B8ED0" # Bleu standard CTk
THEME_COLOR_SUCCESS = "#2CC985" # Vert
THEME_COLOR_WARNING = "#E5A00D" # Orange/Jaune
THEME_TABLE_BG = ("gray90", "gray13") # Fond de la table
THEME_HEADER_BG = ("gray85", "gray17") # Fond du header

class GameView(ctk.CTkFrame):
    """!
    @brief Vue principale du jeu, redesignée pour un alignement et une esthétique modernes.
    @details Affiche la table de jeu, les slots des joueurs, et la main (deck).
    """

    def __init__(self, parent, controller):
        """!
        @brief Constructeur de la GameView.
        @param parent Widget parent.
        @param controller Contrôleur associé (GameController).
        """
        super().__init__(parent, fg_color=THEME_TABLE_BG)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ============================================================
        # 1. HEADER : Informations sur la Feature et le Tour
        # ============================================================
        self.header_frame = ctk.CTkFrame(self, fg_color=THEME_HEADER_BG, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew", ipady=10)
        self.header_frame.grid_columnconfigure(1, weight=1)

        # Titre de la Feature
        self.lbl_feature_title = ctk.CTkLabel(self.header_frame, text="USER STORY EN COURS :", 
                                              font=("Roboto Medium", 12, "bold"), text_color="gray")
        self.lbl_feature_title.grid(row=0, column=0, sticky="w", padx=(20, 5))
        
        self.lbl_feature = ctk.CTkLabel(self.header_frame, text="Chargement...", 
                                        font=("Roboto Medium", 20), wraplength=600, justify="left")
        self.lbl_feature.grid(row=1, column=0, sticky="w", padx=(20, 5))

        # Info du Tour et Règle
        self.info_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.info_box.grid(row=0, column=1, rowspan=2, sticky="e", padx=20)
        
        self.lbl_round_num = ctk.CTkLabel(self.info_box, text="Tour 1", font=("Arial", 24, "bold"), text_color=THEME_COLOR_ACCENT)
        self.lbl_round_num.pack(anchor="e")
        self.lbl_round_rule = ctk.CTkLabel(self.info_box, text="Règle : Unanimité", font=("Arial", 14))
        self.lbl_round_rule.pack(anchor="e")

        # Barre d'instruction centrale
        self.lbl_instruction_bar = ctk.CTkLabel(self, text="", font=("Arial", 16, "bold"), 
                                                height=30, fg_color=("gray80", "gray20"))
        self.lbl_instruction_bar.grid(row=1, column=0, sticky="new")


        # ============================================================
        # 2. TABLE CENTRALE : Zone des joueurs et résultats
        # ============================================================
        self.table_area = ctk.CTkFrame(self, fg_color="transparent")
        self.table_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=(40, 10))
        
        self.table_area.grid_rowconfigure(0, weight=1)
        self.table_area.grid_columnconfigure(0, weight=1)

        # Conteneur horizontal pour les joueurs
        self.players_container = ctk.CTkFrame(self.table_area, fg_color="transparent")
        self.players_container.grid(row=0, column=0, sticky="s")

        # Conteneur pour le résultat central
        self.center_result_container = ctk.CTkFrame(self.table_area, fg_color="transparent")
        self.center_result_container.grid(row=1, column=0, sticky="n", pady=(20, 0))


        # ============================================================
        # 3. DECK : Main du joueur (Bas)
        # ============================================================
        self.deck_container = ctk.CTkFrame(self, height=180, fg_color=("gray85", "gray15"), corner_radius=15)
        self.deck_container.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
        self.deck_container.grid_propagate(False)

        ctk.CTkLabel(self.deck_container, text="VOTRE MAIN", font=("Arial", 12, "bold"), text_color="gray").pack(pady=(10, 0))

        self.scroll_deck = ctk.CTkScrollableFrame(self.deck_container, orientation="horizontal", fg_color="transparent", height=130)
        self.scroll_deck.pack(fill="both", expand=True, padx=10, pady=5)

    # ============================================================
    # MÉTHODES DE MISE À JOUR UI
    # ============================================================

    def refresh_ui(self):
        """!
        @brief Met à jour l'ensemble de l'interface en fonction de l'état du contrôleur.
        @details Rafraîchit le header, la phase de jeu (vote ou résultat) et le deck.
        """
        feature = self.controller.get_current_feature_name()
        if not feature: return

        # 1. Mise à jour Header
        self.lbl_feature.configure(text=feature)
        
        round_num = self.controller.model.current_round_number
        rule_text = "Unanimité requise" if round_num == 1 else self.controller.model.rules.selected_mode
        self.lbl_round_num.configure(text=f"Tour {round_num}")
        self.lbl_round_rule.configure(text=rule_text)

        # 2. Mise à jour Instruction Bar et Contenu Central
        current_player_name = self.controller.get_current_player_name()

        if self.controller.revealed:
            self.lbl_instruction_bar.configure(text="RÉSULTATS DU VOTE", text_color=THEME_COLOR_ACCENT)
            self._show_results_phase()
        else:
            self.lbl_instruction_bar.configure(text=f"C'EST À {current_player_name.upper()} DE VOTER", text_color=THEME_COLOR_WARNING)
            self._show_voting_phase()

    def _show_voting_phase(self):
        """!
        @brief Affiche la phase de vote.
        @details Dessine les slots joueurs avec leur statut (Attente / Réfléchit / A voté).
        """
        for w in self.players_container.winfo_children(): w.destroy()
        for w in self.center_result_container.winfo_children(): w.destroy()

        votes = self.controller.get_votes()
        players = self.controller.model.get_player_names()
        current_voter = self.controller.get_current_player_name()
        
        for i, name in enumerate(players):
            # Slot joueur
            slot = ctk.CTkFrame(self.players_container, width=PLAYER_SLOT_WIDTH, fg_color="transparent")
            slot.pack(side="left", padx=10)
            slot.grid_propagate(False)

            # Nom du joueur
            is_active = (name == current_voter)
            name_color = THEME_COLOR_ACCENT if is_active else "gray"
            ctk.CTkLabel(slot, text=name, font=("Arial", 14, "bold"), text_color=name_color).pack(pady=(0, 10))

            # Zone de statut (Taille carte fixe)
            # CORRECTION : On gère la bordure via border_width=0 au lieu de border_color="transparent"
            border_width = 2 if is_active else 0
            border_color = THEME_COLOR_ACCENT if is_active else None # None ou une couleur valide, ignoré si width=0

            status_box = ctk.CTkFrame(slot, width=CARD_SIZE_TABLE[0], height=CARD_SIZE_TABLE[1], 
                                      fg_color=("gray90", "gray25"), corner_radius=8, 
                                      border_width=border_width,
                                      border_color=border_color)
            status_box.pack()
            status_box.pack_propagate(False)

            if name in votes:
                ctk.CTkLabel(status_box, text="✅", font=("Arial", 40)).pack(expand=True)
                ctk.CTkLabel(slot, text="A voté", font=("Arial", 12), text_color=THEME_COLOR_SUCCESS).pack(pady=(5,0))
            elif is_active:
                ctk.CTkLabel(status_box, text="🤔", font=("Arial", 40)).pack(expand=True)
                ctk.CTkLabel(slot, text="Réfléchit...", font=("Arial", 12), text_color=THEME_COLOR_WARNING).pack(pady=(5,0))
            else:
                ctk.CTkLabel(status_box, text="...", font=("Arial", 40), text_color="gray").pack(expand=True)
                ctk.CTkLabel(slot, text="Attente", font=("Arial", 12), text_color="gray").pack(pady=(5,0))

        self._build_deck(enabled=True)

    def _show_results_phase(self):
        """!
        @brief Affiche la phase de résultats.
        @details Révèle les cartes des joueurs et affiche le panneau de résultat central.
        """
        for w in self.players_container.winfo_children(): w.destroy()
        for w in self.center_result_container.winfo_children(): w.destroy()
        
        votes = self.controller.get_votes()
        
        # 1. Ré-afficher les slots avec les cartes
        for i, (name, val) in enumerate(votes.items()):
            slot = ctk.CTkFrame(self.players_container, width=PLAYER_SLOT_WIDTH, fg_color="transparent")
            slot.pack(side="left", padx=10)

            ctk.CTkLabel(slot, text=name, font=("Arial", 14, "bold")).pack(pady=(0, 10))

            card_btn = self._create_card_button(slot, val, None, size=CARD_SIZE_TABLE)
            card_btn.configure(state="disabled", border_width=0, fg_color="transparent")
            
            card_frame = ctk.CTkFrame(slot, fg_color="transparent", border_width=3, border_color=("gray80", "gray30"), corner_radius=10)
            card_btn.pack(in_=card_frame, padx=3, pady=3)
            card_frame.pack()

        # 2. Panneau de Résultat Central
        result = self.controller.handle_end_of_round()
        
        result_panel = ctk.CTkFrame(self.center_result_container, corner_radius=15, border_width=2)
        result_panel.pack(pady=20, ipadx=30, ipady=15)

        if result == "COFFEE":
            return # Géré par le contrôleur

        elif result == "REVOTE":
            result_panel.configure(border_color=THEME_COLOR_WARNING)
            ctk.CTkLabel(result_panel, text="⚠️ Pas de consensus", font=("Roboto Medium", 18), text_color=THEME_COLOR_WARNING).pack(pady=(0, 10))
            ctk.CTkLabel(result_panel, text="Les estimations sont trop divergentes.\nUne discussion est nécessaire avant de revoter.", justify="center").pack(pady=(0, 15))
            
            ctk.CTkButton(result_panel, text="Relancer le vote (Tour suivant)", 
                                     font=("Arial", 14, "bold"), height=40,
                                     fg_color=THEME_COLOR_WARNING, hover_color="#C4880B",
                                     command=self.controller.restart_round).pack()
        
        else:
            result_panel.configure(border_color=THEME_COLOR_SUCCESS)
            ctk.CTkLabel(result_panel, text="ESTIMATION VALIDÉE", font=("Roboto Medium", 16), text_color=THEME_COLOR_SUCCESS).pack(pady=(0, 5))
            
            res_display = result
            if result == "cafe": res_display = "☕"
            if result == "interro": res_display = "?"
            ctk.CTkLabel(result_panel, text=str(res_display), font=("Roboto Medium", 48, "bold"), text_color=THEME_COLOR_SUCCESS).pack(pady=10)
            
            ctk.CTkButton(result_panel, text="Valider & User Story Suivante", 
                                         font=("Arial", 14, "bold"), height=45, width=220,
                                         fg_color=THEME_COLOR_SUCCESS, hover_color="#229A65",
                                         command=lambda: self.controller.validate_feature(result)).pack()

        self._build_deck(enabled=False)

    # ============================================================
    # GESTION DES CARTES (Deck et Création)
    # ============================================================

    def _build_deck(self, enabled):
        """!
        @brief Construit le deck de cartes cliquables.
        @param enabled Indique si les cartes doivent être actives (cliquables).
        """
        for w in self.scroll_deck.winfo_children(): w.destroy()
        
        for val in self.controller.deck:
            cmd = lambda v=val: self._on_vote(v) if enabled else None
            btn = self._create_card_button(self.scroll_deck, val, cmd, size=CARD_SIZE_DECK)
            
            if not enabled:
                btn.configure(state="disabled", fg_color=("gray85", "gray25"))
            else:
                btn.configure(hover_color=THEME_COLOR_ACCENT, border_color=THEME_COLOR_ACCENT)

            btn.pack(side="left", padx=8, pady=10)

    def _on_vote(self, val):
        """!
        @brief Callback lors du clic sur une carte du deck.
        @param val La valeur de la carte.
        """
        self.controller.cast_vote(val)
        if self.controller.is_round_finished():
            self.controller.revealed = True
        self.refresh_ui()

    def _create_card_button(self, parent, value, command, size):
        """!
        @brief Crée un widget carte (Bouton).
        @details Tente de charger l'image SVG correspondante. En cas d'échec ou d'absence de lib, crée une version texte stylisée.
        @param parent Widget parent.
        @param value Valeur de la carte (ex: '20', 'cafe').
        @param command Fonction à appeler au clic.
        @param size Tuple (largeur, hauteur).
        @return Le widget bouton configuré.
        """
        filename = f"cartes_{value}.svg"
        image_path = f"src/img/{filename}"
        
        ctk_image = None
        
        # --- TENTATIVE CHARGEMENT SVG ---
        if CAIROSVG_AVAILABLE and os.path.exists(image_path):
            try:
                with open(image_path, 'rb') as f: svg_data = f.read()
                png_data = cairosvg.svg2png(bytestring=svg_data, output_height=size[1]*2)
                pil_image = Image.open(io.BytesIO(png_data))
                ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=size)
            except Exception as e:
                print(f"Erreur chargement image {filename}: {e}")

        # --- CRÉATION DU WIDGET ---
        if ctk_image:
            # CORRECTION : border_width=0 pour éviter les problèmes de transparence
            return ctk.CTkButton(parent, text="", image=ctk_image, command=command, 
                                 width=size[0], height=size[1], 
                                 fg_color="transparent", border_width=0,
                                 hover_color=("gray90", "gray30"))
        else:
            display_text = value
            if value == "cafe": display_text = "☕"
            if value == "interro": display_text = "?"
            
            is_special = value in ["cafe", "interro"]
            text_color = THEME_COLOR_ACCENT if not is_special else THEME_COLOR_WARNING
            
            return ctk.CTkButton(parent, text=display_text, command=command,
                                 width=size[0], height=size[1], corner_radius=12,
                                 font=("Arial", 28 if not is_special else 40, "bold"),
                                 border_width=3, border_color=text_color,
                                 fg_color=("white", "gray20"), text_color=text_color,
                                 hover_color=text_color)