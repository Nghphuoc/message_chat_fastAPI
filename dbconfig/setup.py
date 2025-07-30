from fastapi.params import Depends
from sqlalchemy.orm import Session
from dbconfig.config import get_db
from model import Role

def check_create_role(db: Session):
    required_roles = ["MODERATOR", "ADMIN"]
    existing_roles = db.query(Role.role_name).filter(Role.role_name.in_(required_roles)).all()
    existing_role_names = {r.role_name for r in existing_roles}

    for role_name in required_roles:
        if role_name not in existing_role_names:
            db.add(Role(role_name=role_name))

    db.commit()

