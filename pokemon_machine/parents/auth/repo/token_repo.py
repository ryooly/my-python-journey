from sqlalchemy.orm import Session, func
from parents.auth.models.refresh_token import RefreshToken

class TokenRepository:
    def __init__(self, db: Session):
        self.db = db;

        async def create_refresh_token(self, refresh_token: str) -> str:
            self.db.add(refresh_token)
            self.db.commit()
            self.db.refresh(refresh_token)
            return "Create Refresh Token Success"

        async def get_refresh_token_by_token(self, token: str) -> RefreshToken | None:
            return self.db.query(RefreshToken).filter(RefreshToken.token == token).first();

        async def get_refresh_token_by_user_id(self, user_id: int) -> RefreshToken | None:
            return self.db.query(RefreshToken).filter(RefreshToken.user_id == user_id).first();
        
        async def revoke_refresh_token(self, user_id: int) -> str:
            return self.db.query(RefreshToken).filter(RefreshToken.user_id == user_id).update({
                "is_revoked": True, "revoked_at": func.now()
                });
            self.db.commit()

        

        

            
