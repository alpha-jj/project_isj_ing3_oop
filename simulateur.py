# -*- coding: utf-8 -*-
"""
Created on Wed May 20 08:17:54 2026

@author: alexa
"""

from collections import deque

class Simulateur:
    """ Gere la circulation des paquets dans le reseau"""
    def __init__(self, topologie):

        self.topologie = topologie

        self.paquets_envoyes = 0
        self.paquets_perdus = 0
        self.debit_cumule = 0
    def _get_eq(self, ip):
        """ Recherche un equipement a partir de son adresse IP"""
        for eq in self.topologie.equipements:
            if eq.ip == ip:
                return eq

        return None
    
    def trouver_chemin(self, ip_source, ip_dest):
        """ Trouve le chemin le plus court entre deux equipements avec l'algorithme BFS"""
        debut = self._get_eq(ip_source)
        fin = self._get_eq(ip_dest)

        if not debut or not fin:
            return None

        file = deque([[debut]])

        visites = {debut}

        while file:

            chemin = file.popleft()

            noeud = chemin[-1]

            if noeud == fin:
                return chemin

            for voisin in self.topologie.voisins(noeud):

                if voisin not in visites:

                    visites.add(voisin)

                    nouveau_chemin = chemin + [voisin]

                    file.append(nouveau_chemin)

        return None
    
    def envoyer_paquet(self, paquet):
        """ Envoie un paquet dans la topologie reseau"""
        chemin = self.trouver_chemin(
            paquet.source,
            paquet.destination
        )

        if chemin is None:

            print("Destination inatteignable !")
            self.paquets_perdus += 1

            return

        print("Chemin trouvé :")

        for eq in chemin:

            print(f" --> {eq.nom} ({eq.ip})")

        self.paquets_envoyes += 1

        self.debit_cumule += paquet.taille