from abc import ABCMeta, abstractmethod
from typing import Annotated

from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from pydantic import ValidationError

from fwdi.Application.Abstractions.base_user_repository import BaseUserRepositoryFWDI
from fwdi.Application.DTO.Auth.model_user import User
from fwdi.Utilites.jwt_tools import JwtToolsFWDI

oauth2_scheme:OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

class BaseJwtServiceFWDI(metaclass=ABCMeta):
    
    @staticmethod
    @abstractmethod
    def authenticate_user(db_context:BaseUserRepositoryFWDI, username: str, password: str, jwt_tools:JwtToolsFWDI):
        ...

    @staticmethod
    @abstractmethod
    def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)], jwt_tools:JwtToolsFWDI=Depends()):
        ...
    
    @staticmethod
    @abstractmethod
    def get_current_active_user(current_user:User = Security(get_current_user),):
        ...
