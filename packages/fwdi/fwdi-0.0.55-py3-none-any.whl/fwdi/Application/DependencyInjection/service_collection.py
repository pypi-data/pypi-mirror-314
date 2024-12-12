#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from typing import overload

from ...Application.Abstractions.base_di_container import BaseDIConteinerFWDI
from ...Application.Abstractions.base_service_collection import BaseServiceCollectionFWDI
from ...Application.Abstractions.service_descriptor import ServiceDescriptorFWDI
from ...Domain.Enums.service_life import ServiceLifetime
from .dependency_container import DependencyContainerFWDI, TService

class ServiceCollectionFWDI(BaseServiceCollectionFWDI):
    def __init__(self) -> None:        
        self._serviceDescriptor:set[ServiceDescriptorFWDI] = set()

    @property
    def ServiceDescriptor(self)->set:
        return self._serviceDescriptor

#====================================================================================================================================================
    @overload
    def AddSingleton(self, instance:TService):
        ...

    @overload
    def AddSingleton(self, inst_type:type[TService]):
        ...
    
    def AddSingleton(self, base_type:type[TService]=None, inst_type:type[TService]=None)->TService:
        self.__add(ServiceLifetime.Singleton, base_type, inst_type)

    #===========================================================================================

    @overload
    def AddTransient(self, inst_type:type[TService]):
        ...

    def AddTransient(self, base_type:type[TService]=None, inst_type:type[TService]=None):
        self.__add(ServiceLifetime.Transient, base_type, inst_type)

    def __add(self, lifetime:ServiceLifetime, base_type:type[TService]=None, inst_type:type[TService]=None):
        from ...Utilites.ext_reflection import ExtReflection
        if ExtReflection.is_class(base_type):
            if base_type != None and inst_type != None:
                self._serviceDescriptor.add(ServiceDescriptorFWDI.create(base_type, inst_type, lifetime))
            elif base_type != None and inst_type == None:
                self._serviceDescriptor.add(ServiceDescriptorFWDI.create_from_type(base_type, lifetime))
        else:
            if lifetime == ServiceLifetime.Singleton:
                self._serviceDescriptor.add(ServiceDescriptorFWDI.create_from_instance(base_type, lifetime))
            else:
                raise Exception('Error !!! Instance registration is allowed only for Singleton !')

#====================================================================================================================================================

    def GenerateContainer(self)->BaseDIConteinerFWDI:
        return DependencyContainerFWDI(self._serviceDescriptor)