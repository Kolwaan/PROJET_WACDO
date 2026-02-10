#
# Script pour initialiser la base de données avec des utilisateurs de test
# À exécuter après chaque suppression de la base de données

# Ce script crée un utilisateur pour chaque rôle disponible dans l'application.

# Commande --> python seed_database.py

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
            "description": "Administrateur principal (accès complet)"
        },
        {
            "nom": "Superviseur Test",
            "email": "superviseur@test.com",
            "password": "123",
            "role": RoleEnum.SUPERVISEUR_DE_PREPARATION,
            "description": "Superviseur de préparation (gestion des commandes)"
        },
        {
            "nom": "Agent Préparation Test",
            "email": "preparateur@test.com",
            "password": "123",
            "role": RoleEnum.AGENT_DE_PREPARATION,
            "description": "Agent de préparation (prépare les commandes)"
        },
        {
            "nom": "Agent Accueil Test",
            "email": "accueil@test.com",
            "password": "123",
            "role": RoleEnum.AGENT_ACCUEIL,
            "description": "Agent d'accueil (crée et livre les commandes)"
        }
    ]
    
    created_count = 0
    skipped_count = 0
    
    try:
        for user_data in users_to_create:
            # Vérifier si l'utilisateur existe déjà
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            
            if existing:
                print(f"⏭️  {user_data['email']} existe déjà (ID: {existing.id}), ignoré")
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
            
            print(f"✅ Créé : {user.email}")
            print(f"   └─ Nom: {user.nom}")
            print(f"   └─ Rôle: {user.role.value}")
            print(f"   └─ ID: {user.id}")
            print(f"   └─ Description: {user_data['description']}")
            print()
            
            created_count += 1
        
        print("=" * 60)
        print(f"🎉 Initialisation terminée !")
        print(f"   ✅ Utilisateurs créés : {created_count}")
        print(f"   ⏭️  Utilisateurs existants : {skipped_count}")
        print("=" * 60)
        
        if created_count > 0:
            print("\n🔐 Connexion sur Swagger :")
            print("   1. Allez sur http://localhost:8000/docs")
            print("   2. Trouvez POST /auth/token")
            print("   3. Utilisez ces identifiants :")
            print()
            print("   Admin :")
            print("   └─ username: boss@test.com")
            print("   └─ password: 123")
            print()
            print("   Superviseur :")
            print("   └─ username: superviseur@test.com")
            print("   └─ password: 123")
            print()
            print("   Préparateur :")
            print("   └─ username: preparateur@test.com")
            print("   └─ password: 123")
            print()
            print("   Accueil :")
            print("   └─ username: accueil@test.com")
            print("   └─ password: 123")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de l'initialisation : {e}")
    
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 INITIALISATION DE LA BASE DE DONNÉES")
    print("=" * 60)
    print()
    seed_users()
