#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from .routeble import RoutebleFWDI
from ...Utilites.ext_controller import ExtController

from ...Utilites.ext_reflection import ExtReflection

class BaseRoutebleFWDI(RoutebleFWDI):   
    def __init__(self, base_path:str='/'):
        super().__init__()
        self.base_path:str = base_path
        self.__object:object = self
        self.__create_endpoint(type(self))

    def __create_endpoint(self, type_inst:type):
        path_name = ExtController.get_controller_name(type_inst.__name__)

        lst_method = ExtReflection.list_class_methods(type_inst, False)
        for item in lst_method:
            name, method = item
            method = ExtReflection.get_handler_method(self.__object, name)
            self.add_api_route(f"{self.base_path}{path_name}", method, methods=[name.upper()]) # use decorator