#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

#------INTERFACES-----------------------------------------------------------
from fwdi.Application.Abstractions.base_jwt_service import BaseJwtServiceFWDI
from fwdi.Infrastructure.JwtService.jwt_service import JwtServiceFWDI
from ..Application.Abstractions.base_service_collection import BaseServiceCollectionFWDI
from ..Application.Abstractions.base_rest_client import BaseRestClientFWDI
#------/INTERFACES----------------------------------------------------------

#-----INSTANCE--------------------------------------------------------------
from ..Infrastructure.Rest.rest_client import RestClientFWDI
#-----/INSTANCE-------------------------------------------------------------

class DependencyInjection():
    def AddInfrastructure(services:BaseServiceCollectionFWDI)->None:
        services.AddTransient(BaseRestClientFWDI, RestClientFWDI)
        services.AddTransient(BaseJwtServiceFWDI, JwtServiceFWDI)