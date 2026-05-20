"""
moniteur.py

Surveillance du réseau et génération de rapports d'exploitation.

Classes :
    Moniteur — collecte les statistiques et génère rapport_simnet.txt
"""

from collections import deque
from datetime import datetime


class Moniteur:
    """
    Moniteur réseau de SIMNet.

    Collecte en temps réel :
        - paquets transmis / perdus par équipement
        - taux d'utilisation de chaque lien
        - liste des équipements actifs et inactifs
        - historique des 10 derniers paquets (deque à taille fixe)

    Génère à la demande un rapport d'exploitation (rapport_simnet.txt).
    """

    def __init__(self, topologie, simulateur):
        self.topologie       = topologie
        self.simulateur      = simulateur
        # deque(maxlen=10) : garde automatiquement les 10 dernières entrées
        self.historique      = deque(maxlen=10)
        # stats par équipement : {nom: {"envoyes": 0, "perdus": 0}}
        self.stats_par_eq: dict = {}

    # ── Enregistrement ────────────────────────────────────────────────────────

    def enregistrer_paquet(self, paquet, chemin: list, succes: bool):
        """
        Enregistre un paquet dans l'historique et met à jour les stats
        de chaque équipement du chemin.

        Paramètres :
            paquet  : objet Paquet transmis
            chemin  : liste d'équipements traversés
            succes  : True si livré, False si perdu/bloqué
        """
        ts    = datetime.now().strftime("%H:%M:%S")
        etat  = "OK" if succes else "PERDU"
        entree = f"[{ts}] [{etat}] {paquet}"
        self.historique.append(entree)

        for eq in chemin:
            if eq.nom not in self.stats_par_eq:
                self.stats_par_eq[eq.nom] = {"envoyes": 0, "perdus": 0}
            if succes:
                self.stats_par_eq[eq.nom]["envoyes"] += 1
            else:
                self.stats_par_eq[eq.nom]["perdus"]  += 1

    # ── Affichage console ─────────────────────────────────────────────────────

    def afficher_stats(self):
        """Affiche un tableau de bord complet dans le terminal."""
        print("\n" + "=" * 55)
        print("       TABLEAU DE BORD — Moniteur SIMNet")
        print("=" * 55)

        # Statistiques globales
        total = (self.simulateur.paquets_envoyes
                 + self.simulateur.paquets_perdus)
        taux  = (self.simulateur.paquets_perdus / total * 100) if total > 0 else 0
        print(f"\n  GLOBALES :")
        print(f"    Paquets envoyés  : {self.simulateur.paquets_envoyes}")
        print(f"    Paquets perdus   : {self.simulateur.paquets_perdus}")
        print(f"    Taux de perte    : {taux:.1f} %")
        print(f"    Débit cumulé     : {self.simulateur.debit_cumule} octets")

        # Équipements actifs / inactifs
        actifs   = [e for e in self.topologie.equipements if e.statut]
        inactifs = [e for e in self.topologie.equipements if not e.statut]
        print(f"\n  ÉQUIPEMENTS ACTIFS ({len(actifs)}) :")
        for e in actifs:
            print(f" {e.nom} ({e.ip})")
        if inactifs:
            print(f"\n  ÉQUIPEMENTS INACTIFS ({len(inactifs)}) :")
            for e in inactifs:
                print(f"  {e.nom} ({e.ip})")

        # Taux d'utilisation des liens
        print(f"\n  LIENS ({len(self.topologie.liens)}) :")
        for lien in self.topologie.liens:
            print(f"    {lien.eq1.nom} ←→ {lien.eq2.nom} | "
                  f"Utilisation : {lien.utilisation():.1f} % | "
                  f"BP : {lien.bande_passante} Mbps")

        # Stats par équipement
        if self.stats_par_eq:
            print(f"\n  STATS PAR ÉQUIPEMENT :")
            for nom, s in self.stats_par_eq.items():
                print(f"    {nom} — envoyés: {s['envoyes']}, perdus: {s['perdus']}")

        # Historique des 10 derniers paquets
        print(f"\n  DERNIERS PAQUETS (max 10) :")
        if not self.historique:
            print("    (aucun paquet enregistré)")
        for h in self.historique:
            print(f"    {h}")

        print("=" * 55)

    # ── Génération du rapport ────────────────────────────────────────────────

    def generer_rapport(self, nom_fichier: str = "rapport_simnet.txt"):
        """
        Génère un fichier texte complet d'exploitation réseau.
        Enregistré dans le répertoire courant sous le nom fourni.
        """
        now   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total = (self.simulateur.paquets_envoyes
                 + self.simulateur.paquets_perdus)
        taux  = (self.simulateur.paquets_perdus / total * 100) if total > 0 else 0

        with open(nom_fichier, "w", encoding="utf-8") as f:

            f.write("=" * 60 + "\n")
            f.write("          RAPPORT D'EXPLOITATION — SIMNet\n")
            f.write(f"          Généré le : {now}\n")
            f.write("=" * 60 + "\n\n")

            # Statistiques globales
            f.write("1. STATISTIQUES GLOBALES\n")
            f.write("-" * 40 + "\n")
            f.write(f"   Paquets envoyés   : {self.simulateur.paquets_envoyes}\n")
            f.write(f"   Paquets perdus    : {self.simulateur.paquets_perdus}\n")
            f.write(f"   Taux de perte     : {taux:.1f} %\n")
            f.write(f"   Débit cumulé      : {self.simulateur.debit_cumule} octets\n")
            f.write(f"   Temps de transit  : {self.simulateur.temps_transit:.1f} ms\n\n")

            # Équipements
            f.write("2. ÉQUIPEMENTS DU RÉSEAU\n")
            f.write("-" * 40 + "\n")
            for eq in self.topologie.equipements:
                etat = "ACTIF" if eq.statut else "INACTIF"
                f.write(f"   [{etat}] {eq.infos()}\n")
            f.write("\n")

            # Liens
            f.write("3. LIENS ET UTILISATION\n")
            f.write("-" * 40 + "\n")
            for lien in self.topologie.liens:
                f.write(f"   {lien.eq1.nom} ←→ {lien.eq2.nom} | "
                        f"BP: {lien.bande_passante} Mbps | "
                        f"Latence: {lien.latence} ms | "
                        f"Utilisation: {lien.utilisation():.1f} %\n")
            f.write("\n")

            # Stats par équipement
            f.write("4. STATS PAR ÉQUIPEMENT\n")
            f.write("-" * 40 + "\n")
            if self.stats_par_eq:
                for nom, s in self.stats_par_eq.items():
                    f.write(f"   {nom} — envoyés: {s['envoyes']}, perdus: {s['perdus']}\n")
            else:
                f.write("   (aucune donnée)\n")
            f.write("\n")

            # Historique
            f.write("5. HISTORIQUE DES 10 DERNIERS PAQUETS\n")
            f.write("-" * 40 + "\n")
            if self.historique:
                for h in self.historique:
                    f.write(f"   {h}\n")
            else:
                f.write("   (aucun paquet enregistré)\n")
            f.write("\n")

            f.write("=" * 60 + "\n")
            f.write("          FIN DU RAPPORT\n")
            f.write("=" * 60 + "\n")

        print(f"  Rapport généré : '{nom_fichier}'")
