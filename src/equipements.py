
from abc import ABC, abstractmethod
import re

class Equipement(ABC):

    def __init__(self, nom: str, ip: str, marque: str, statut: bool = True):
        self.nom    = nom
        self.ip     = self._valider_ip(ip)
        self.marque = marque
        self.statut = statut

    def _valider_ip(self, ip: str) -> str:
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, ip):
            raise ValueError(f"Adresse IP invalide : '{ip}'")
        octets = ip.split('.')
        for octet in octets:
            if not (0 <= int(octet) <= 255):
                raise ValueError(f"Octet hors limite dans l'IP : '{ip}'")
        return ip

    @abstractmethod
    def infos(self) -> str:
        """Retourne un résumé lisible de l'équipement."""
        pass

    def __str__(self) -> str:
        etat = "ACTIF" if self.statut else "INACTIF"
        return f"[{etat}] {self.nom} ({self.ip}) — {self.marque}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(nom={self.nom!r}, ip={self.ip!r})"

    def activer(self):
        self.statut = True
        print(f"✔  {self.nom} activé.")

    def desactiver(self):
        """Désactive l'équipement."""
        self.statut = False
        print(f"✘  {self.nom} désactivé.")

class Routeur(Equipement):

    def __init__(self, nom: str, ip: str, marque: str):
        super().__init__(nom, ip, marque)
        self.table_routage: dict = {} 

    def ajouter_route(self, destination: str, prochain_saut: str):
        self.table_routage[destination] = prochain_saut
        print(f"  Route ajoutée : {destination} via {prochain_saut}")

    def supprimer_route(self, destination: str):
        """Supprime une route de la table."""
        if destination in self.table_routage:
            del self.table_routage[destination]
            print(f"  Route supprimée : {destination}")
        else:
            print(f"  Route introuvable : {destination}")

    def afficher_table(self):
        """Affiche la table de routage."""
        print(f"\n  Table de routage de {self.nom} :")
        if not self.table_routage:
            print("    (vide)")
        for dest, saut in self.table_routage.items():
            print(f"    {dest}  →  {saut}")

    def infos(self) -> str:
        return (f"Routeur '{self.nom}' | IP: {self.ip} | "
                f"Marque: {self.marque} | Routes: {len(self.table_routage)}")

class Switch(Equipement):

    def __init__(self, nom: str, ip: str, marque: str, nb_ports: int = 24):
        super().__init__(nom, ip, marque)
        self.nb_ports = nb_ports
        self.vlans: list = []  
    def ajouter_vlan(self, vlan_id: int):
        if vlan_id in self.vlans:
            print(f"  VLAN {vlan_id} déjà présent.")
        else:
            self.vlans.append(vlan_id)
            print(f"  VLAN {vlan_id} ajouté sur {self.nom}.")

    def supprimer_vlan(self, vlan_id: int):
        """Supprime un VLAN du switch."""
        if vlan_id in self.vlans:
            self.vlans.remove(vlan_id)
            print(f"  VLAN {vlan_id} supprimé.")
        else:
            print(f"  VLAN {vlan_id} introuvable.")

    def infos(self) -> str:
        return (f"Switch '{self.nom}' | IP: {self.ip} | "
                f"Marque: {self.marque} | Ports: {self.nb_ports} | "
                f"VLANs: {self.vlans}")

class Serveur(Equipement):

    def __init__(self, nom: str, ip: str, marque: str):
        super().__init__(nom, ip, marque)
        self.services: list = []   # ex: ["HTTP:80", "SSH:22"]

    def ajouter_service(self, service: str):
        """Ajoute un service exposé par le serveur."""
        self.services.append(service)
        print(f"  Service '{service}' ajouté sur {self.nom}.")

    def supprimer_service(self, service: str):
        """Supprime un service."""
        if service in self.services:
            self.services.remove(service)
            print(f"  Service '{service}' supprimé.")
        else:
            print(f"  Service '{service}' introuvable.")

    def infos(self) -> str:
        return (f"Serveur '{self.nom}' | IP: {self.ip} | "
                f"Marque: {self.marque} | Services: {self.services}")

class Firewall(Equipement):


    def __init__(self, nom: str, ip: str, marque: str,
                 login: str = "admin", mdp: str = "admin123"):
        super().__init__(nom, ip, marque)
        self._login = login 
        self._mdp   = mdp 
        self.regles: list  = [] 
        self.journal: list = [] 

    def authentifier(self, login: str, mdp: str) -> bool:
        return login == self._login and mdp == self._mdp

    def ajouter_regle(self, regle, login: str, mdp: str):
        if not self.authentifier(login, mdp):
            raise PermissionError("Accès refusé : identifiants incorrects.")
        self.regles.append(regle)
        print(f"  Règle ajoutée : {regle}")

    def inspecter(self, paquet) -> bool:
        from src.securite import RegleFirewall
        for regle in self.regles:
            if regle.correspond(paquet):
                decision = regle.action
                self._journaliser(decision, paquet, regle)
                if decision == "BLOQUER":
                    return False 
                else:
                    return True 
        self._journaliser("AUTORISE (défaut)", paquet, None)
        return True

    def _journaliser(self, action: str, paquet, regle):
        from datetime import datetime
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = (f"[{ts}] {action} | "
               f"{paquet.source} → {paquet.destination} | "
               f"Proto: {paquet.protocole} | "
               f"Règle: {regle if regle else 'défaut'}")
        self.journal.append(msg)

    def afficher_journal(self):
        print(f"\n  Journal du Firewall '{self.nom}' :")
        if not self.journal:
            print("    (vide)")
        for entree in self.journal:
            print(f"    {entree}")

    def infos(self) -> str:
        return (f"Firewall '{self.nom}' | IP: {self.ip} | "
                f"Marque: {self.marque} | Règles: {len(self.regles)}")

class PointAccesWifi(Equipement):

    def __init__(self, nom: str, ip: str, marque: str,
                 ssid: str = "SIMNet-WiFi", frequence: str = "2.4 GHz"):
        super().__init__(nom, ip, marque)
        self.ssid      = ssid
        self.frequence = frequence

    def infos(self) -> str:
        return (f"WiFi '{self.nom}' | IP: {self.ip} | "
                f"SSID: {self.ssid} | Fréquence: {self.frequence} | "
                f"Marque: {self.marque}")

class Terminal(Equipement):

    def __init__(self, nom: str, ip: str, marque: str, utilisateur: str = "inconnu"):
        super().__init__(nom, ip, marque)
        self.utilisateur = utilisateur

    def infos(self) -> str:
        return (f"Terminal '{self.nom}' | IP: {self.ip} | "
                f"Utilisateur: {self.utilisateur} | Marque: {self.marque}")
