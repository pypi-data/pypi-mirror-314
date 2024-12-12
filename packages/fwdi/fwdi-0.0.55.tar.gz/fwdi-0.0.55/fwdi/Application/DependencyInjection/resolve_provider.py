#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from ...Application.Abstractions.base_di_container import BaseDIConteinerFWDI, TService

class ResolveProviderFWDI():
    __container:BaseDIConteinerFWDI = None
    __debug:bool = False
    def __init__(self, container:BaseDIConteinerFWDI, debug:bool) -> None:
        if ResolveProviderFWDI.__container == None:
            ResolveProviderFWDI.__container = container
            ResolveProviderFWDI.__debug = debug

    @staticmethod
    def is_init()->bool:
        return False if ResolveProviderFWDI.__container == None else True

    @staticmethod
    def get_service(cls:TService)->TService | None:
        if ResolveProviderFWDI.__container == None:
            raise Exception('Not initialize ResolveProvider !')
        else:
            return ResolveProviderFWDI.__container.GetService(cls)

    @staticmethod
    def contains(cls:TService)->bool:
        if ResolveProviderFWDI.__container == None:
            raise Exception('Not initialize ResolveProvider !')
        else:
            return ResolveProviderFWDI.__container.contains(cls)