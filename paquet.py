

# Paquet



    """
    Représente un paquet réseau.

    Attributs :
        source      (str) : adresse IP source
        destination (str) : adresse IP destination
        protocole   (str) : TCP, UDP ou ICMP
        taille      (int) : taille en octets
        priorite    (int) : niveau de priorité de 1 (basse) à 5 (haute)
        port_dest   (int) : port de destination 
    """

class Paquet:
    """Représente un paquet réseau qui va circuler  dans notre infrastructure."""

    PROTOCOLES_VALIDES = {"TCP", "UDP", "ICMP"}

    def __init__(self, source: str, destination: str, protocole: str = "TCP", 
                 taille: int = 512, priorite: int = 1, port_dest: int = 80):
        
        self.source = source
        self.destination = destination
        self.protocole = self._valider_protocole(protocole)
        self.taille = taille
        self.priorite = self._valider_priorite(priorite)
        self.port_dest = port_dest

    def _valider_protocole(self, protocole: str) -> str:
        """Force le protocole en majuscules et vérifie sa validité."""
        p = protocole.upper()
        if p not in self.PROTOCOLES_VALIDES:
            raise ValueError(f"Protocole invalide : '{protocole}'. Les choix valides sont : {self.PROTOCOLES_VALIDES}")
        return p

    def _valider_priorite(self, priorite: int) -> int:
        """Vérifie que la priorité reste bien comprise entre 1 et 5."""
        if not (1 <= priorite <= 5):
            raise ValueError(f"Priorité invalide : {priorite}. Elle doit être comprise entre 1 et 5.")
        return priorite

    def __str__(self) -> str:
        """Affichage simple et compréhensible pour l'utilisateur ."""
        return (f"[{self.protocole}] {self.source} → {self.destination} | "
                f"Port: {self.port_dest} | Taille: {self.taille} octets | "
                f"Priorité: {self.priorite}")

    def __repr__(self) -> str:
        """Représentation simple"""
        return f"Paquet(source={self.source}, destination={self.destination}, protocole={self.protocole})"