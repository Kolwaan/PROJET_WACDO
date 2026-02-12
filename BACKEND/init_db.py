"""
Script pour initialiser la base de données en production.
À exécuter APRÈS le premier déploiement sur Render.
"""
import os
import sys

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine
from app.models import User, Product, Menu, Order, MenuProduct, OrderMenu, OrderProduct

def init_database():
    """
    Crée toutes les tables dans la base de données.
    """
    print("🔨 Création des tables dans la base de données...")
    
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tables créées avec succès !")
        print("\nTables créées :")
        for table in Base.metadata.sorted_tables:
            print(f"  - {table.name}")
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables : {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database()
