# seed_database.py
# Initialise la base de données avec des données de démonstration propres.
#
# Commande : python seed_database.py

from app.database import SessionLocal
from app.models.user import User
from app.models.product import Product
from app.models.menu import Menu
from app.enums.role import RoleEnum
from app.enums.type import ProductType
from app.enums.menu_type import MenuType
from app.utils.hash import hash_password


# ─────────────────────────────────────────────
# UTILISATEURS
# ─────────────────────────────────────────────

def seed_users(db):

    users_to_create = [
        {"nom": "Alice Martin",   "email": "admin@wacdo.fr",        "password": "123", "role": RoleEnum.ADMINISTRATEUR},
        {"nom": "Bruno Dupont",   "email": "superviseur@wacdo.fr",  "password": "123", "role": RoleEnum.SUPERVISEUR_DE_PREPARATION},
        {"nom": "Clara Petit",    "email": "preparateur@wacdo.fr",  "password": "123",  "role": RoleEnum.AGENT_DE_PREPARATION},
        {"nom": "David Moreau",   "email": "accueil@wacdo.fr",      "password": "123", "role": RoleEnum.AGENT_ACCUEIL},
    ]

    created, skipped = 0, 0

    for u in users_to_create:
        existing = db.query(User).filter(User.email == u["email"]).first()
        if existing:
            print(f"  [SKIP] {u['email']} existe déjà")
            skipped += 1
            continue
        user = User(
            nom=u["nom"],
            email=u["email"],
            password=hash_password(u["password"]),
            role=u["role"]
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"  [OK] {user.email} — {user.role.value}")
        created += 1

    return created, skipped


# ─────────────────────────────────────────────
# PRODUITS (15 au total)
# ─────────────────────────────────────────────
#
# Répartition :
#   4 burgers        → PRODUIT_UNIQUE
#   3 boissons       → BOISSON
#   3 frites/sides   → PRODUIT_UNIQUE
#   2 sauces         → PRODUIT_UNIQUE
#   2 desserts       → PRODUIT_UNIQUE
#   1 wrap           → PRODUIT_UNIQUE

def seed_products(db):

    products_to_create = [
        # Burgers
        {"nom": "Big Mac",              "prixHT": 6.00,  "image": "/burgers/BIGMAC.png",               "type": ProductType.PRODUIT_UNIQUE},
        {"nom": "Royal Cheese",         "prixHT": 4.40,  "image": "/burgers/ROYALCHEESE.png",          "type": ProductType.PRODUIT_UNIQUE},
        {"nom": "MC Crispy",            "prixHT": 5.30,  "image": "/burgers/MCCRISPY.png",             "type": ProductType.PRODUIT_UNIQUE},
        {"nom": "CBO",                  "prixHT": 8.90,  "image": "/burgers/CBO.png",                  "type": ProductType.PRODUIT_UNIQUE},
        # Boissons
        {"nom": "Coca Cola",            "prixHT": 1.90,  "image": "/boissons/coca-cola.png",           "type": ProductType.BOISSON},
        {"nom": "Fanta Orange",         "prixHT": 1.90,  "image": "/boissons/fanta.png",               "type": ProductType.BOISSON},
        {"nom": "Eau",                  "prixHT": 1.00,  "image": "/boissons/eau.png",                 "type": ProductType.BOISSON},
        # Frites / sides
        {"nom": "Petite Frite",         "prixHT": 1.45,  "image": "/frites/PETITE_FRITE.png",         "type": ProductType.PRODUIT_UNIQUE},
        {"nom": "Moyenne Frite",        "prixHT": 2.75,  "image": "/frites/MOYENNE_FRITE.png",        "type": ProductType.PRODUIT_UNIQUE},
        {"nom": "Potatoes",             "prixHT": 2.15,  "image": "/frites/POTATOES.png",             "type": ProductType.PRODUIT_UNIQUE},
        # Sauces
        {"nom": "Ketchup",              "prixHT": 0.70,  "image": "/sauces/ketchup.png",              "type": ProductType.PRODUIT_UNIQUE},
        {"nom": "Classic Barbecue",     "prixHT": 0.70,  "image": "/sauces/classic-barbecue.png",     "type": ProductType.PRODUIT_UNIQUE},
        # Desserts
        {"nom": "Cookie",               "prixHT": 3.20,  "image": "/desserts/cookie.png",             "type": ProductType.PRODUIT_UNIQUE},
        {"nom": "MC Fleury",            "prixHT": 4.40,  "image": "/desserts/MCFleury.png",           "type": ProductType.PRODUIT_UNIQUE},
        # Wrap
        {"nom": "MC Wrap Poulet Bacon", "prixHT": 3.30,  "image": "/wraps/MCWRAP-POULET-BACON.png",  "type": ProductType.PRODUIT_UNIQUE},
    ]

    created, skipped = 0, 0

    for p in products_to_create:
        existing = db.query(Product).filter(Product.nom == p["nom"]).first()
        if existing:
            print(f"  [SKIP] {p['nom']} existe déjà")
            skipped += 1
            continue
        product = Product(
            nom=p["nom"],
            prixHT=p["prixHT"],
            image=p["image"],
            type=p["type"],
            disponibilite=True,
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        print(f"  [OK] {product.nom} — {product.prixHT}€")
        created += 1

    return created, skipped


# ─────────────────────────────────────────────
# MENUS
# ─────────────────────────────────────────────
#
# Chaque menu est composé de :
#   1 burger  +  1 frite ou potatoes  +  1 sauce  +  1 boisson
#
# BEST_OF      → Petite Frite
# MAXI_BEST_OF → Moyenne Frite ou Potatoes

def seed_menus(db):

    def get(nom):
        p = db.query(Product).filter(Product.nom == nom).first()
        if not p:
            raise ValueError(f"Produit introuvable : '{nom}' — lance d'abord seed_products()")
        return p

    big_mac       = get("Big Mac")
    royal_cheese  = get("Royal Cheese")
    mc_crispy     = get("MC Crispy")
    coca          = get("Coca Cola")
    fanta         = get("Fanta Orange")
    petite_frite  = get("Petite Frite")
    moyenne_frite = get("Moyenne Frite")
    potatoes      = get("Potatoes")
    ketchup       = get("Ketchup")
    barbecue      = get("Classic Barbecue")

    menus_to_create = [
        {
            "nom": "Menu Big Mac",
            "description": "Big Mac, Petite Frite, Ketchup, Coca Cola",
            "prixHT": 8.00,
            "image": "/burgers/BIGMAC.png",
            "menu_type": MenuType.BEST_OF,
            "produits": [big_mac, petite_frite, ketchup, coca],
        },
        {
            "nom": "Menu Royal Cheese",
            "description": "Royal Cheese, Petite Frite, Barbecue, Fanta Orange",
            "prixHT": 7.20,
            "image": "/burgers/ROYALCHEESE.png",
            "menu_type": MenuType.BEST_OF,
            "produits": [royal_cheese, petite_frite, barbecue, fanta],
        },
        {
            "nom": "Maxi Menu Big Mac",
            "description": "Big Mac, Moyenne Frite, Ketchup, Coca Cola",
            "prixHT": 9.50,
            "image": "/burgers/BIGMAC.png",
            "menu_type": MenuType.MAXI_BEST_OF,
            "produits": [big_mac, moyenne_frite, ketchup, coca],
        },
        {
            "nom": "Maxi Menu MC Crispy",
            "description": "MC Crispy, Potatoes, Barbecue, Fanta Orange",
            "prixHT": 9.80,
            "image": "/burgers/MCCRISPY.png",
            "menu_type": MenuType.MAXI_BEST_OF,
            "produits": [mc_crispy, potatoes, barbecue, fanta],
        },
    ]

    created, skipped = 0, 0

    for m in menus_to_create:
        existing = db.query(Menu).filter(Menu.nom == m["nom"]).first()
        if existing:
            print(f"  [SKIP] {m['nom']} existe déjà")
            skipped += 1
            continue
        menu = Menu(
            nom=m["nom"],
            description=m["description"],
            prixHT=m["prixHT"],
            image=m["image"],
            disponibilite=True,
            menu_type=m["menu_type"],
            produits=m["produits"],
        )
        db.add(menu)
        db.commit()
        db.refresh(menu)
        contenu = ", ".join(p.nom for p in menu.produits)
        print(f"  [OK] {menu.nom} ({menu.menu_type.value}) → {contenu}")
        created += 1

    return created, skipped


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    db = SessionLocal()

    try:
        print("\n" + "=" * 60)
        print("SEED — UTILISATEURS")
        print("=" * 60)
        u_created, u_skipped = seed_users(db)

        print("\n" + "=" * 60)
        print("SEED — PRODUITS")
        print("=" * 60)
        p_created, p_skipped = seed_products(db)

        print("\n" + "=" * 60)
        print("SEED — MENUS")
        print("=" * 60)
        m_created, m_skipped = seed_menus(db)

        print("\n" + "=" * 60)
        print("RÉSUMÉ")
        print("=" * 60)
        print(f"Utilisateurs créés : {u_created}  |  déjà existants : {u_skipped}")
        print(f"Produits créés     : {p_created}  |  déjà existants : {p_skipped}")
        print(f"Menus créés        : {m_created}  |  déjà existants : {m_skipped}")
        print("\nIdentifiants de connexion :")
        print("  admin@wacdo.fr        /  Admin2026!  (ADMINISTRATEUR)")
        print("  superviseur@wacdo.fr  /  Super2026!  (SUPERVISEUR)")
        print("  preparateur@wacdo.fr  /  Prep2026!   (AGENT_PREPARATION)")
        print("  accueil@wacdo.fr      /  Accueil26!  (AGENT_ACCUEIL)")
        print("=" * 60 + "\n")

    except Exception as e:
        db.rollback()
        print(f"\n[ERREUR] {e}")
        raise

    finally:
        db.close()
