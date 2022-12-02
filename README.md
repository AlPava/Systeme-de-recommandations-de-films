# :movie_camera: Systeme-de-recommandations-de-fims
*Projet étudiant - tableau de bord et machine learning avec Python*

## :beginner: Sujet
Un cinéma fictif en perte de vitesse situé dans la Creuse nous a confié la tâche de créer:
- un moteur de recommandations de films qui à terme, enverra des notifications aux clients via internet
- un tableau de bord proposant des indicateurs donnant une vision détaillée de la base de données utilisée

Aucun client n’a renseigné ses préférences : situation de cold start.
Le client nous a donné une base de données de films basée sur la plateforme IMDb.

## :dart: Fonctionnalités

Le département de la Creuse a la moyenne d'âge la plus élevée de la région.  
Notre application propose ainsi des films adaptés à cette population : films des années 1970 à 2010.

![Picture1](Pictures/) **< photo page d'accueil streamlit**

### :bar_chart: Page 'Admin'

Cette page est constituée de 4 onglets contenant des indicateurs à propos du nombre de films, de leur durée enfonction du genre, etc...
Certains graphiques sont intéracifs grâce aux filtres disponibles.

### :massage: Page 'Profil utilisateur'

Les recommandations de films aux utilisateurs se font sur cette page.  
L'utilisateur sélectionne un ou plusieurs genres. L'agorithme lui propose 5 films aléatoires pour chaque genre.  
Puis l'utilisateur choisit un film de liste : il obtient 5 recommandations de films qui sont les plus proches voisins de celui précédemment sélectionné.

### :underage: Page 'Creuse & Chill'

(Private joke :trollface:)

Ses habitants ne possèdent pas systématiquement l'accès aux technologies et à internet.  
Ainsi, cette page leur propose aléatoirement 5 titres de films pour adultes diffusés par le Ciné'Creuse.  
La page est protégée par un mot de passe stocké dans .streamlit/secrets.toml

## :wrench: Tools

![Picture1](Pictures/WorkflowDiagram.png) **< créer un dossier Pictures, y glisser le png du workflow diagram**

## :handshake: Team

<a href="https://github.com/HeEmilie" target="_blank" rel="noopener noreferrer"><img src="https://crd.so/i/HeEmilie?dark&removeLink" alt="HeEmilie’s GitHub image" width="400" height="208.5" />
<a href="https://github.com/AlPava" target="_blank" rel="noopener noreferrer"><img src="https://crd.so/i/AlPava?dark&removeLink" alt="AlPava’s GitHub image" width="400" height="208.5" />
<a href="https://github.com/florentdm" target="_blank" rel="noopener noreferrer"><img src="https://crd.so/i/florentdm?dark&removeLink" alt="florentdm’s GitHub image" width="400" height="208.5" />
<a href="https://github.com/VarlamV" target="_blank" rel="noopener noreferrer"><img src="https://crd.so/i/VarlamV?dark&removeLink" alt="VarlamV’s GitHub image" width="400" height="208.5" />

## :clapper: Démonstration

![VideoDemo](Pictures/Dashboard_head_page.png) **< ajouter une vidéo de demo !**

## :rocket: Perspectives


