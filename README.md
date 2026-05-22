# SIMNet — Simulateur de Réseau Intelligent

> Projet de groupe — Programmation Orientée Objet en Python
> **INGÉNIEUR 3 SRT** · Institut Saint Jean · Année académique 2025-2026

---

## Description

Ce dépôt est le point de départ officiel du projet **SIMNet**, donné aux étudiants
de 3ème année Génie Télécom & Réseaux dans le cadre du cours de Programmation Orientée
Objet en Python.

**SIMNet** est un simulateur de réseau d'entreprise entièrement orienté objet. Il permet
de modéliser une topologie réseau, de faire circuler des paquets entre équipements,
d'en assurer la sécurité via un firewall, et d'en superviser le fonctionnement grâce
à un moniteur réseau.

---

## Structure attendue du projet

Chaque groupe doit organiser son code selon la structure suivante :

```
project_isj_ing3_oop/
│
├── src/
│   ├── equipements.py      # Classes des équipements réseau
│   ├── topologie.py        # Topologie et liens
│   ├── paquets.py          # Paquet et simulation de trafic
│   ├── securite.py         # Firewall, règles, journal
│   ├── moniteur.py         # Moniteur réseau et rapports
│   └── main.py             # Point d'entrée et menu interactif
│
├── rapport.pdf             # Rapport technique du groupe
└── README.md               # Ce fichier (à compléter par le groupe)
```

---

## Lancement

```bash
python src/main.py
```

> Python 3.8+ requis. Aucune dépendance externe.

---

##  Workflow de soumission

### 1. Forker le dépôt

Cliquer sur **Fork** en haut à droite de cette page.
Un seul membre du groupe effectue le fork.

### 2. Cloner le fork

```bash
git clone https://github.com/<votre-compte>/project_isj_ing3_oop.git
cd project_isj_ing3_oop
```

### 3. Créer la branche du groupe

Le nom de branche doit correspondre **exactement** à votre numéro de groupe :

```bash
git checkout -b group_1   # adapter : group_1, group_2, group_3 ...
```

### 4. Développer et committer régulièrement

```bash
git add .
git commit -m "feat: ajout de la classe Routeur et de la topologie"
git push origin group_1
```

> Un historique de commits régulier est attendu. Un seul commit massif
> en fin de semaine sera pénalisé.

### 5. Ouvrir une Merge Request

Depuis votre fork, ouvrir une **Merge Request** vers la branche `main` du
dépôt officiel `st9-8/project_isj_ing3_oop`.

- **Titre :** `[Groupe X] SIMNet — NomDuGroupe`
- **Description :** fonctionnalités implémentées, noms des membres, remarques éventuelles

> Ne pas merger la Merge Request vous-même. Elle sera consultée et validée
> par l'examinateur lors de la correction.

---

## Modules fonctionnels

| Module | Description |
|--------|-------------|
| 1 — Modélisation | Équipements réseau, topologie, liens |
| 2 — Trafic | Paquets, routage saut par saut, statistiques |
| 3 — Sécurité | Firewall, règles de filtrage, journal horodaté |
| 4 — Surveillance | Moniteur réseau, métriques, export rapport |
| 5 — Interface | Menu console interactif |

---

## Groupes

| Branche | Groupe | Membres |
|---------|--------|---------|
| `group_1` | — | — |
| `group_2` | — | — |
| `group_3` | — | — |
| `group_4` | — | — |
| `group_5` | — | — |

> Ce tableau sera mis à jour par l'examinateur au démarrage du projet.

---

## Évaluation

| Critère | Points |
|---------|--------|
| Fonctionnement du simulateur | 6 |
| Qualité de la modélisation POO | 5 |
| Couverture des concepts du cours | 4 |
| Rapport technique | 3 |
| Soutenance et maîtrise individuelle | 2 |
| **Total** | **20** |

---

##  Examinateur

**M. Stephane Fedim**  
Institut Saint Jean - Parcours Ingénieur
Année académique 2025-2026 · Semestre 2
git status

