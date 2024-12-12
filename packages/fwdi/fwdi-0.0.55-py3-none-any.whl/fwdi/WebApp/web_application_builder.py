#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from typing import TypeVar
from fastapi.security import OAuth2PasswordBearer

from ..Application.Abstractions.base_service_collection import BaseServiceCollectionFWDI
from ..Application.DependencyInjection.resolve_provider import ResolveProviderFWDI
from ..Application.DependencyInjection.service_collection import ServiceCollectionFWDI
from ..Infrastructure.JwtService.jwt_service import JwtServiceFWDI
from ..Persistence.default_init_db import DefaultInitializeDB
from ..Utilites.system_logging import SysLogging, TypeLogging

T = TypeVar('T')
__log__ = SysLogging(logging_level=TypeLogging.DEBUG, filename='WebApplicationBuilder')

class WebApplicationBuilder():
    def __init__(self, obj:T) -> None:
        __log__(f"{__name__}:{obj}")
        self.__instance_app:type[T] = obj
        self.services:BaseServiceCollectionFWDI = ServiceCollectionFWDI()
        self.__scopes:dict[str, str] = {}

    def build(self)-> type[T]:
        __log__(f"Build services")
        from ..Presentation.dependency_injection import DependencyInjection as DependencyInjectionPresentation
        from ..Utilites.dependency_injection import DependencyInjection as DependencyInjectionUtilites
        
        self.__instance_app.instance = self
        self.__instance_app.resolver = ResolveProviderFWDI(self.services.GenerateContainer(), self.__instance_app.Debug)
        
        #---------------------- DEFAULT WEB CONTROLLER SERVICES ------------------------------------
        __log__(f"Create dependency injection Utilites")
        DependencyInjectionUtilites.AddUtilites(self.services)
        __log__(f"Create dependency injection Presentation")
        DependencyInjectionPresentation.AddPresentation(self.__instance_app)

        #---------------------- /DEFAULT WEB CONTROLLER SERVICES -----------------------------------
        __log__(f"Inititalize OAuth2PasswordBearer: scope:{self.__scopes}")
        JwtServiceFWDI.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes=self.__scopes,) if len(self.__scopes) > 0 else OAuth2PasswordBearer(tokenUrl="token")
        __log__(f"Inititalize DB")
        DefaultInitializeDB.init_db(self.__scopes)
        return self.__instance_app
    
    def add_scope(self, scopes:dict[str,str]):
        for item in scopes.items():
            if not item in self.__scopes:
                self.__scopes[item[0]] = item[1]
    
    def add_authentification(self):
        ...
        
    def add_health_checks(self):
        ...
    
    def add_httpclient(self):
        ...

    def add_logging(self):
        ...