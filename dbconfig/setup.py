from sqlalchemy.orm import Session
from model.Role import Role, RoleType  # đảm bảo đúng import
import uuid
from datetime import datetime

def check_create_role(db: Session):
    required_roles = [RoleType.ADMIN.value, RoleType.MODERATOR.value]

    existing_roles = db.query(Role.role_name).filter(Role.role_name.in_(required_roles)).all()
    existing_role_names = {role.role_name for role in existing_roles}

    for role_name in required_roles:
        if role_name not in existing_role_names:
            role = Role(
                role_id=str(uuid.uuid4()),
                role_name=role_name,
                create_time=datetime.utcnow()
            )
            db.add(role)
            print(f"[INFO] Created role: {role_name}")
        else:
            print(f"[INFO] Role already exists: {role_name}")

    db.commit()
