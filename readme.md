# PROJET WACDO
[![Voir le projet](https://img.shields.io/badge/WACDO-Live%20Demo-blue?style=for-the-badge)](https://wacdo-kolwaan.alwaysdata.net/)

## Description
Application web simulant une borne de commande de restauration rapide.
L’utilisateur peut sélectionner des produits, composer un panier et finaliser une commande.

## Fichiers fournis
Assets : fichiers images
Data : listes des produits et des catégories (au format JSON)

## Fichiers html
index.html : choix sur place ou à emporter
chevalet.html : saisie du numéro de chevalet
choix.html : lites des choix (menus, burgers, boissons, dessert, etc.)
merci.html : page de remerciements avec redirection vers une nouvelle commande

## Fichiers css 
CSS/style.css : styles des pages : acceuil.html, chevalet.html et merci.html
CSS/style2.css : style de la page choix.html
CSS/style3.css : styles des pages : chevalet.html, merci.html (bouton)
CSS/style4.css : style de la page merci.html

## Fichier JavaScript
JS/main.js : script de la page des choix
JS/slider.js : script pour les sliders (catégories et boissons)

## Fichiers image
### Images boissons
ASSETS/boissons/coca-cola.png
ASSETS/boissons/coca-sans-sucres.png
ASSETS/boissons/eau.png
ASSETS/boissons/fanta.png
ASSETS/boissons/ice-tea-peche.png
ASSETS/boissons/jus-orange.png
ASSETS/boissons/jus-pomme-bio.png
ASSETS/boissons/the-vert-citron-sans-sucres.png

### Images burgers
ASSETS/burgers/280.png
ASSETS/burgers/BIGMAC.png
ASSETS/burgers/BIG_TASTY_1_VIANDE.png
ASSETS/burgers/BIG_TASTY_BACON_1_VIANDE.png
ASSETS/burgers/CBO.png
ASSETS/burgers/MCCHICKEN.png
ASSETS/burgers/MCCRISPY.png
ASSETS/burgers/MCFISH.png
ASSETS/burgers/ROYALBACON.png
ASSETS/burgers/ROYALCHEESE.png
ASSETS/burgers/ROYALDELUXE.png
ASSETS/burgers/SIGNATURE_BBQ_BEEF_(2_VIANDES).png
ASSETS/burgers/SIGNATURE_BEEF_BBQ_BURGER_(1_VIANDE).png

### Images catégories
ASSETS/categories/boissons.png
ASSETS/categories/burgers.png
ASSETS/categories/desserts.png
ASSETS/categories/encas.png
ASSETS/categories/frites.png
ASSETS/categories/menus.png
ASSETS/categories/salades.png
ASSETS/categories/sauces.png
ASSETS/categories/wraps.png

### Images desserts
ASSETS/desserts/brownies.png
ASSETS/desserts/cheesecake_choconuts_M&M_s.png
ASSETS/desserts/cheesecake_fraise.png
ASSETS/desserts/cookie.png
ASSETS/desserts/doghnut.png
ASSETS/desserts/macarons.png
ASSETS/desserts/MCFleury.png
ASSETS/desserts/muffin.png
ASSETS/desserts/sunday.png

### Images encas
ASSETS/encas/cheeseburger.png
ASSETS/encas/croc-mc-do.png
ASSETS/encas/nuggets_20.png
ASSETS/encas/nuggets_4.png

### Images frites
ASSETS/frites/GRANDE_FRITE.png
ASSETS/frites/GRANDE_POTATOES.png
ASSETS/frites/MOYENNE_FRITE.png
ASSETS/frites/PETITE_FRITE.png
ASSETS/frites/POTATOES.png

### Images navigation, logos et bannière
ASSETS/images/chevalet_wacdo.png
ASSETS/images/fleche-slider.png
ASSETS/images/illustration-a-emporter.png
ASSETS/images/illustration-best-of.png
ASSETS/images/illustration-maxi-best-of.png
ASSETS/images/illustration-sur-place.png
ASSETS/images/logo.png
ASSETS/images/mc_landing_banner.png
ASSETS/images/supprimer.png
ASSETS/images/trash.png

### Images salades
ASSETS/salades/PETITE-SALADE.png
ASSETS/salades/SALADE_CLASSIC_CAESAR.png
ASSETS/salades/SALADE_ITALIAN_MOZZA.png

### Images sauces
ASSETS/sauces/classic-barbecue.png
ASSETS/sauces/classic-moutarde.png
ASSETS/sauces/cremy-deluxe.png
ASSETS/sauces/ketchup.png
ASSETS/sauces/sauce-chinoise.png
ASSETS/sauces/sauce-curry.png
ASSETS/sauces/sauce-pommes-frite.png

### Images wraps
ASSETS/wraps/mcwrap-chevre.png
ASSETS/wraps/MCWRAP-POULET-BACON.png
ASSETS/wraps/PTIT_WRAP_CHEVRE.png
ASSETS/wraps/PTIT_WRAP_RANCH.png


## Données du projet
Les fichiers JSON utilisés par le site se trouvent dans le dossier : DATA/

Liste des fichiers JSON :
- DATA/categories.json : menus affichés dans le slider
- DATA/produits.json : ensemble des produits disponibles

Pour tester l'accessibilité des données en local :
http://localhost:5501/DATA/categories.json
http://localhost:5501/DATA/produits.json

En production :
https://wacdo-kolwaan.alwaysdata.net/data/categories.json
https://wacdo-kolwaan.alwaysdata.net/data/produits.json

## Chargement des données
Les données des produits sont stockées dans des fichiers JSON et sont chargées dynamiquement côté client à l’aide de l’interface Fetch fournie par le navigateur (requêtes HTTP / AJAX).
Les fichiers de données étant hébergés sur le même domaine que l’application, aucun problème de CORS ne se pose.

## Technologies utilisées
  - HTML5
  - CSS3
  - JavaScript (ES6)
  - JSON
  - Web APIs (Fetch / AJAX)

## Lien public vers le prototype figma
https://www.figma.com/design/0qnd0pH4qryZqjzXcB4qjN/borne?node-id=97-775&t=SJ4QkHUyIRA5QSb0-1

