
from collections import deque

class Lien:
    Représente un lien physique entre deux équipements.

    Attributs :
        eq1 : premier équipement (objet Equipement)
        eq2 : deuxième équipement (objet Equipement)
        bande_passante : capacité en Mbps
        latence : délai en ms

    def __init__(self, eq1, eq2, bande_passante: float = 100.0, latence: float = 1.0):
        self.eq1 = eq1
        self.eq2 = eq2
        self.bande_passante  = bande_passante
        self.latence = latence
        self.octets_transmis = 0

    def utilisation(self) -> float:
        if self.bande_passante == 0:
            return 0.0
        mbits = (self.octets_transmis * 8) / (1024 * 1024)
        return round(min((mbits / self.bande_passante) * 100, 100.0), 2)

    def __str__(self) -> str:
        return (f"{self.eq1.nom} ←→ {self.eq2.nom} | "
                f"{self.bande_passante} Mbps | {self.latence} ms")

    def __repr__(self) -> str:
        return f"Lien({self.eq1.nom!r}, {self.eq2.nom!r})"

class Topologie:
    def __init__(self):
        self.equipements: list = []
        self.liens: list = [] 


    def ajouter_equipement(self, eq):
        for e in self.equipements:
            if e.ip == eq.ip:
                raise ValueError(f"IP déjà utilisée : {eq.ip}")
        self.equipements.append(eq)
        print(f"Équipement ajouté : {eq}")

    def supprimer_equipement(self, nom: str):

        eq = self.get_equipement_par_nom(nom)
        if eq is None:
            print(f"  Équipement '{nom}' introuvable.")
            return
        # Supprimer les liens associés
        self.liens = [l for l in self.liens if l.eq1 != eq and l.eq2 != eq]
        self.equipements.remove(eq)
        print(f"Équipement '{nom}' et ses liens supprimés.")

    def get_equipement_par_nom(self, nom: str):
        for eq in self.equipements:
            if eq.nom == nom:
                return eq
        return None

    def get_equipement_par_ip(self, ip: str):
        for eq in self.equipements:
            if eq.ip == ip:
                return eq
        return None

    def ajouter_lien(self, nom_eq1: str, nom_eq2: str,
                     bande_passante: float = 100.0, latence: float = 1.0):
        eq1 = self.get_equipement_par_nom(nom_eq1)
        eq2 = self.get_equipement_par_nom(nom_eq2)
        if eq1 is None:
            print(f"Équipement '{nom_eq1}' introuvable.")
            return
        if eq2 is None:
            print(f"Équipement '{nom_eq2}' introuvable.")
            return
        lien = Lien(eq1, eq2, bande_passante, latence)
        self.liens.append(lien)
        print(f" Lien ajouté : {lien}")

    def supprimer_lien(self, nom_eq1: str, nom_eq2: str):
        for lien in self.liens:
            if ({lien.eq1.nom, lien.eq2.nom} == {nom_eq1, nom_eq2}):
                self.liens.remove(lien)
                print(f"Lien supprimé entre {nom_eq1} et {nom_eq2}.")
                return
        print(f"  Lien introuvable entre {nom_eq1} et {nom_eq2}.")

    def get_lien(self, eq1, eq2):
        for lien in self.liens:
            if {lien.eq1, lien.eq2} == {eq1, eq2}:
                return lien
        return None

    def voisins(self, eq) -> list:""
        voisins = []
        for lien in self.liens:
            if lien.eq1 == eq and lien.eq2.statut:
                voisins.append(lien.eq2)
            elif lien.eq2 == eq and lien.eq1.statut:
                voisins.append(lien.eq1)
        return voisins

    def afficher(self):
        print("\n" + "=" * 55)
        print("TOPOLOGIE DU RÉSEAU — SIMNet")
        print("=" * 55)

        print(f"\nÉQUIPEMENTS ({len(self.equipements)}) :")
        if not self.equipements:
            print("    (aucun équipement)")
        for eq in self.equipements:
            print(f"• {eq}")

        print(f"\n  LIENS ({len(self.liens)}) :")
        if not self.liens:
            print(" (aucun lien)")
        for lien in self.liens:
            print(f"─ {lien}")

        print("=" * 55)
