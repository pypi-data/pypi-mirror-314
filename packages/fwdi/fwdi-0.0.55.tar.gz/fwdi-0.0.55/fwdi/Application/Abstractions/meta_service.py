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

class MetaServiceFWDI(type):
    def __init__(cls, name, bases, ns):
        from ...Utilites.system_logging import SysLogging, TypeLogging
        from ...Utilites.ext_reflection import ExtReflection
        for attr, value in cls.__dict__.items():
            if callable(value):
                if attr == '__call__':
                    setattr(cls, attr, ExtReflection.init_inject(value))
                    
                if not attr.startswith('__') and not inspect.isabstract(cls):
                    setattr(cls, attr, ExtReflection._inject_(value))
        
        if not inspect.isabstract(cls):
            if hasattr(cls, '__name__'):
                cls.__log__ = SysLogging(logging_level=TypeLogging.DEBUG, filename=cls.__name__)
        
        super().__init__(name, bases, ns)