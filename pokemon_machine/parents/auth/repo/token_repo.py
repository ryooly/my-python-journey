from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from parents.auth.models.refresh_token import RefreshToken


class TokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_refresh_token(self, token: str, user_id: int) -> str:
        refresh = RefreshToken(token=token, user_id=user_id)
        self.db.add(refresh)
        self.db.commit()
        self.db.refresh(refresh)
        return "Create Refresh Token Success"

    def get_refresh_token_by_user_id(self, user_id: int) -> RefreshToken | None:
        return self.db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == 0,
        ).first()

    def revoke_refresh_token(self, user_id: int) -> None:
        self.db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
        ).update({"is_revoked": 1})
        self.db.commit()
