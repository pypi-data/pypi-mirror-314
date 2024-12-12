from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import SecurityScopes
from jwt.exceptions import InvalidTokenError

from pydantic import ValidationError

from fwdi.Application.Abstractions.base_jwt_service import BaseJwtServiceFWDI, oauth2_scheme

from ...Application.Abstractions.base_user_repository import BaseUserRepositoryFWDI
from ...Application.DTO.Auth.model_user import User
from ...Application.DTO.Auth.token_data import TokenData
from ...Persistence.manager_db_context import ManagerDbContextFWDI
from ...Utilites.jwt_tools import JwtToolsFWDI


class JwtServiceFWDI(BaseJwtServiceFWDI):

    @staticmethod
    def authenticate_user(db_context:BaseUserRepositoryFWDI, username: str, password: str, jwt_tools:JwtToolsFWDI):
        JwtServiceFWDI.__log__(f"{__name__}:{db_context}:{username}:{password}")
        user = jwt_tools.get_user_by_username(db_context, username)
        JwtServiceFWDI.__log__(f"Auth:{user}")

        if not user:
            return False
        if not jwt_tools.verify_password(password, user.hashed_password):
            return False
        
        return user
    
    @staticmethod
    def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)], jwt_tools:JwtToolsFWDI=Depends()):
        JwtServiceFWDI.__log__(f"{__name__}:{security_scopes}:{token}")
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"' if security_scopes.scopes else "Bearer"
        JwtServiceFWDI.__log__(f"{__name__}:{authenticate_value}")

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )

        try:
            payload = jwt_tools.decode_payload_token(token)
            JwtServiceFWDI.__log__(f"{__name__}:{payload}")
            username: str = payload.get("sub")
            email: str = payload.get("email")
            if username is None:
                raise credentials_exception
            token_scopes = payload.get("scopes", [])
            token_data = TokenData(scopes=token_scopes, username=username, email=email)
            JwtServiceFWDI.__log__(f"{__name__}:{token_data}")

        except (InvalidTokenError, ValidationError) as ex:
            JwtServiceFWDI.__log__(ex)
            raise credentials_exception
        
        users_db = ManagerDbContextFWDI().get_metadata_user()
        user = jwt_tools.get_user_by_email(users_db, email=token_data.email)
        JwtServiceFWDI.__log__(f"{__name__}:{user}")

        if user is None:
            JwtServiceFWDI.__log__(f"User not found :{users_db}")
            raise credentials_exception
        
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                JwtServiceFWDI.__log__(f"{user}:Not enough permissions")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        
        return user
    
    @staticmethod
    def get_current_active_user(current_user:User = Security(get_current_user),):
        JwtServiceFWDI.__log__(f"{__name__}:{current_user}")
        if current_user.disabled:
            JwtServiceFWDI.__log__(f"400, Inactive user")
            raise HTTPException(status_code=400, detail="Inactive user")
        
        return current_user