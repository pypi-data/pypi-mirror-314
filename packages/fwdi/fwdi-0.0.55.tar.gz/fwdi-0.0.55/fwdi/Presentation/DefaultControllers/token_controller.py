#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

import inspect
from typing import Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ...Application.Usecase.user_repository import UserRepositoryFWDI
from ...Application.Abstractions.meta_service import MetaServiceFWDI
from ...Application.DTO.Auth.token import Token
from ...Infrastructure.JwtService.jwt_service import JwtServiceFWDI

from ...Utilites.jwt_tools import JwtToolsFWDI

class TokenController(metaclass=MetaServiceFWDI):
    
    @staticmethod
    def post(user_repository:UserRepositoryFWDI = Depends(), form_data:OAuth2PasswordRequestForm = Depends(), jwt_tools:JwtToolsFWDI = Depends())->Token:
        TokenController.__log__(f"{__name__}:{form_data}","debug")
        all_data = user_repository.get_all()
        user = JwtServiceFWDI.authenticate_user(all_data, form_data.username, form_data.password)

        TokenController.__log__(f"{user}","debug")

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        #--------Using service by created dependency injection service -------

        user_scopes = user_repository.get_user_scopes(user.email)
        TokenController.__log__(f"{user_scopes}","debug")
        #--------/Using service by created dependency injection service ------

        access_token = jwt_tools.create_access_token(
            data={
                "sub": user.username, 
                "email": user.email,
                "scopes": user_scopes
                }
        )
        TokenController.__log__(f"Create token :{access_token}","debug")
        return Token(access_token=access_token, token_type="bearer")