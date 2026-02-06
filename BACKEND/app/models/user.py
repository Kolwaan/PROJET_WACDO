from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
from app.enums.role import RoleEnum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    # --> clef primaire, L'id est généré automatiquement par la base de données (SQLAlchemy)
    # l'id ne doit donc pas être présent lors des tests de création de compte
    nom = Column(String, nullable=False)
    email = Column(String, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum))
