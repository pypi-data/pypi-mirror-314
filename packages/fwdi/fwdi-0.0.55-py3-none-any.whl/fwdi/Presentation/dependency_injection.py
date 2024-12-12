#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from ..WebApp.web_application import WebApplication
from .DefaultControllers.home_controller import Controller
from .DefaultControllers.token_controller import TokenController

class DependencyInjection():
    def AddPresentation(app:WebApplication)->None:
        #------------- HOME ENDPOINTS -----------------------------

        app.map_get(path="/home", endpoint=Controller().index)
        
        #-------------/HOME ENDPOINTS -----------------------------
        #------------- SECURITY ENDPOINTS--------------------------
        
        #app.map_controller(TokenController)
        app.map_post(path='/token', endpoint=TokenController.post)

        #-------------/SECURITY ENDPOINTS--------------------------