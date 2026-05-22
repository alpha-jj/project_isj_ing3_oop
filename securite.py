class RegleFirewall:
    """
    Représente une règle de filtrage appliquée par le Firewall.

    """

    def __init__(self, action: str,
                 ip_source: str    = None,
                 protocole: str    = None,
                 port_dest: int    = None,
                 plage_reseau: str = None,
                 description: str  = ""):

        action = action.upper()
        if action not in {"BLOQUER", "AUTORISER"}:
            raise ValueError(f"Action invalide : '{action}'. "
                             "Valides : BLOQUER, AUTORISER")
        self.action       = action
        self.ip_source    = ip_source
        self.protocole    = protocole.upper() if protocole else None
        self.port_dest    = port_dest
        self.plage_reseau = plage_reseau
        self.description  = description

    def correspond(self, paquet) -> bool:
        """
        Vérifie si ce paquet satisfait tous les  condition de cette règle.
        """
        # Critère : IP source exacte
        if self.ip_source and paquet.source != self.ip_source:
            return False

        # Critère : protocole
        if self.protocole and paquet.protocole != self.protocole:
            return False

        if self.port_dest and paquet.port_dest != self.port_dest:
            return False
        if self.plage_reseau and not paquet.source.startswith(self.plage_reseau):
            return False

        return True   # tous les critères définis correspondent

    def __str__(self) -> str:
        criteres = []
        if self.ip_source:    criteres.append(f"IP={self.ip_source}")
        if self.protocole:    criteres.append(f"Proto={self.protocole}")
        if self.port_dest:    criteres.append(f"Port={self.port_dest}")
        if self.plage_reseau: criteres.append(f"Réseau={self.plage_reseau}*")
        c = ", ".join(criteres) if criteres else "toujours"
        return f"[{self.action}] si {c}" + (f" — {self.description}" if self.description else "")

    def __repr__(self) -> str:
        return f"RegleFirewall(action={self.action})"

class JournalSecurite:
    



    def __init__(self):
        self.entrees: list = []

    def enregistrer(self, action: str, paquet, regle=None):
        """
        Ajoute une entrée dans le journal.

        Paramètres :
            action  : "BLOQUER" ou "AUTORISER (défaut)"
            paquet  : objet Paquet concerné
            
        """
        ts    = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        regle_str = str(regle) if regle else "règle par défaut"
        entree = (f"[{ts}] {action:15s} | "
                  f"{paquet.source} → {paquet.destination} | "
                  f"Proto: {paquet.protocole} | Port: {paquet.port_dest} | "
                  f"Règle: {regle_str}")
        self.entrees.append(entree)

    def afficher(self):
        """Affiche toutes les entrées du journal."""
        print("\n" + "=" * 60)
        print("         JOURNAL DE SÉCURITÉ — Firewall")
        print("=" * 60)
        if not self.entrees:
            print("  (journal vide — aucun paquet inspecté)")
        for e in self.entrees:
            print(f"  {e}")
        print("=" * 60)

    def exporter(self, fichier: str = "journal_firewall.txt"):
        """Exporte le journal dans un fichier texte."""
        with open(fichier, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("  JOURNAL DE SÉCURITÉ — SIMNet Firewall\n")
            f.write(f"  Exporté le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n")
            for e in self.entrees:
                f.write(e + "\n")
        print(f" Journal exporté dans '{fichier}'.")

    def __len__(self) -> int:
        return len(self.entrees)