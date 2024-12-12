#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from abc import ABCMeta, abstractmethod
from typing import TypeVar, overload

from .base_di_container import BaseDIConteinerFWDI

TService = TypeVar('TService')

class BaseServiceCollectionFWDI(metaclass=ABCMeta):

    @overload
    @abstractmethod
    def AddSingleton(self, inst:TService):
        pass

    @overload
    @abstractmethod
    def AddSingleton(self, inst_type:type[TService]):
        pass
    
    #===========================================================================================

    @overload
    @abstractmethod
    def AddTransient(self, base_type:type[TService]):
        pass

    #===========================================================================================
    
    @abstractmethod
    def GenerateContainer(self)->BaseDIConteinerFWDI:
        pass
