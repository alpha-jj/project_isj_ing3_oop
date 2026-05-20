# -*- coding: utf-8 -*-
"""
Created on Wed May 20 10:33:22 2026

@author: alexa
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 20 08:02:24 2026

@author: alexa
"""

# paquets.py

class Paquet:
    """ Represente un paquet reseau circulant dans la topologie"""
    def __init__(self, source, destination,
                 protocole, taille,
                 priorite=1, port_dest=None):

        self.source = source
        self.destination = destination
        self.protocole = protocole.upper()
        self.taille = taille
        self.priorite = priorite
        self.port_dest = port_dest

    def __str__(self):
        return (f"{self.source} -> {self.destination} "
                f"[{self.protocole}] "
                f"{self.taille} octets")
    