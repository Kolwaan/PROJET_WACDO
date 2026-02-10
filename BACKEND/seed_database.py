# Script pour initialiser la base de données avec des utilisateurs de test
# À exécuter après chaque suppression de la base de données

# ⚠️ EN DÉVELOPPEMENT UNIQUEMENT ⚠️
# Les mots de passe sont volontairement simples pour faciliter les tests.
# NE JAMAIS utiliser ce script en production.

# Commande: python seed_database.py


from app.database import SessionLocal
from app.models.user import User
from app.enums.role import RoleEnum
from app.utils.hash import hash_password


# Crée des utilisateurs de test pour tous les rôles
def seed_users():
    
    db = SessionLocal()

    users_to_create = [
        {
            "nom": "Boss",
            "email": "boss@test.com",
            "password": "123",
            "role": RoleEnum.ADMINISTRATEUR,
        },
        {
            "nom": "Superviseur Test",
            "email": "superviseur@test.com",
            "password": "123",
            "role": RoleEnum.SUPERVISEUR_DE_PREPARATION,
        },
        {
            "nom": "Agent Préparation Test",
            "email": "preparateur@test.com",
            "password": "123",
            "role": RoleEnum.AGENT_DE_PREPARATION,
        },
        {
            "nom": "Agent Accueil Test",
            "email": "accueil@test.com",
            "password": "123",
            "role": RoleEnum.AGENT_ACCUEIL,
        }
    ]

    created_count = 0
    skipped_count = 0

    try:
        for user_data in users_to_create:
            # Vérifier si l'utilisateur existe déjà
            existing = db.query(User).filter(User.email == user_data["email"]).first()

            if existing:
                print(f"[SKIP] {user_data['email']} existe déjà (ID: {existing.id})")
                skipped_count += 1
                continue

            # Créer l'utilisateur
            user = User(
                nom=user_data["nom"],
                email=user_data["email"],
                password=hash_password(user_data["password"]),
                role=user_data["role"]
            )

            db.add(user)
            db.commit()
            db.refresh(user)

            print(f"[OK] Utilisateur créé: {user.email} (Role: {user.role.value}, ID: {user.id})")
            created_count += 1

        print("\n" + "="*60)
        print(f"Initialisation terminée")
        print(f"Utilisateurs créés: {created_count}")
        print(f"Utilisateurs existants: {skipped_count}")
        print("="*60)

        if created_count > 0:
            print("\nIdentifiants de connexion (Swagger: http://localhost:8000/docs):")
            print("\nAdmin:")
            print("  username: boss@test.com")
            print("  password: 123")
            print("\nSuperviseur:")
            print("  username: superviseur@test.com")
            print("  password: 123")
            print("\nPréparateur:")
            print("  username: preparateur@test.com")
            print("  password: 123")
            print("\nAccueil:")
            print("  username: accueil@test.com")
            print("  password: 123")

    except Exception as e:
        db.rollback()
        print(f"[ERREUR] {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    print("="*60)
    print("INITIALISATION DE LA BASE DE DONNÉES")
    print("="*60 + "\n")
    seed_users()