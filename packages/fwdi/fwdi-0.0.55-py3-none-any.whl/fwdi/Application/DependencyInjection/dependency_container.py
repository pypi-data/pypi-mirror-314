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
from typing import Type, TypeVar

from ...Application.Abstractions.service_descriptor import ServiceDescriptorFWDI
from ...Application.Abstractions.base_di_container import BaseDIConteinerFWDI
from ...Domain.Enums.service_life import ServiceLifetime

TService = TypeVar('TService')

class DependencyContainerFWDI(BaseDIConteinerFWDI):
    def __init__(self, serviceDescriptors:set) -> None:
        self.__serviceDescriptors:set[ServiceDescriptorFWDI] = serviceDescriptors
    
    def __GetImplementService(self, inst:TService):
        ...

    def contains(self, base_type:type)->bool:
        #=========DEBUG============================================
        """
        print(f"__GetService (serviceType={base_type})")

        for item in self.__serviceDescriptors:
            compare_test = item.ServiceType == base_type
            print(f"{compare_test} compared Item: {item.ServiceType}")
        """
        #=========DEBUG============================================

        descriptor = [item for item in self.__serviceDescriptors if item.ServiceType == base_type]
        return True if len(descriptor) > 0 else False

    def __GetService(self, base_type:type)->TService|None:
        from ...Utilites.ext_reflection import ExtReflection
        #=========DEBUG============================================
        """
        print(f"__GetService (serviceType={base_type})")

        for item in self.__serviceDescriptors:
            compare_test = item.ServiceType == base_type
            print(f"{compare_test} compared Item: {item.ServiceType}")
        """
        #=========DEBUG============================================

        descriptor = [item for item in self.__serviceDescriptors if item.ServiceType == base_type]
        

        if len(descriptor) > 0:
            descriptor = descriptor[0]
        else:
            #raise Exception(f"Service of type {base_type.__name__} isn`t registered !")
            return None
        
        if descriptor.Implementation != None:
            return descriptor.Implementation

        if descriptor.ImplementationType != None:
            actualType = descriptor.ImplementationType
        else:
            actualType = descriptor.ServiceType

        if inspect.isabstract(actualType):
            raise Exception("Cannot instantiate abstract classes.")

        sig = inspect.signature(actualType)
        lst_args_obj = {}

        if len(sig.parameters) > 0:
            for item in sig.parameters:
                annotation = sig.parameters[item].annotation
                implement = self.__GetService(annotation)
                lst_args_obj[item] = implement
        else:
            if self.contains(actualType):
                if ExtReflection.is_injectable_init(actualType):
                    implementation = actualType(**{'is_inject':True})
                else:
                    implementation = actualType()
            else:
                implementation = actualType()

            if descriptor.Lifetime == ServiceLifetime.Singleton:
                descriptor.Implementation = implementation
            return implementation

        if self.contains(actualType):
            if ExtReflection.is_injectable_init(actualType):
                lst_args_obj.update({'is_inject':True})

        implementation = actualType(**lst_args_obj)

        if descriptor.Lifetime == ServiceLifetime.Singleton:
            descriptor.Implementation = implementation

        return implementation

    def GetService(self, cls:Type[TService]) -> TService | None:
        return self.__GetService(cls)