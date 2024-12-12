#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

import time
from functools import wraps
import inspect
import itertools
from types import FunctionType
from typing import Any, TypeVar, Callable

from fwdi.Utilites.global_setting_service import GlobalSettingService, TypeLoggingLevel

from ..Application.DependencyInjection.resolve_provider import *
from ..Domain.Enums.type_methods import TypeMethod
from .utilities import Utilities
from ..Utilites.system_logging import SysLogging

T = TypeVar('T')
_C = TypeVar("_C", bound=Callable[..., Any])

class ExtReflection():
    count_inject:int = 0
    __log__ = SysLogging(filename="__inject__")
    
    @staticmethod
    def get_methods_class(cls):
        return set((x, y) for x, y in cls.__dict__.items()
                    if isinstance(y, (FunctionType, classmethod, staticmethod))
                    and not(x.startswith("__") and x.endswith("__")))

    @staticmethod
    def get_type_method(fn:_C)->TypeMethod:
        is_method = None if not hasattr(fn, '__self__') else False if inspect.isclass(fn.__self__) else True
        match(is_method):
            case None:
                return TypeMethod.Static
            case False:
                return TypeMethod.Classmethod
            case True:
                return TypeMethod.Instance
    
    @staticmethod
    def get_list_parent_methods(cls):
        return set(itertools.chain.from_iterable(
            ExtReflection.get_methods_class(c).union(ExtReflection.get_list_parent_methods(c)) for c in cls.__bases__))

    @staticmethod
    def list_class_methods(cls, is_narrow:bool):
        methods = ExtReflection.get_methods_class(cls)
        if  is_narrow:
            parentMethods = ExtReflection.get_list_parent_methods(cls)
            return set(cls for cls in methods if not (cls in parentMethods))
        else:
            return methods
    
    @staticmethod
    def get_handler_method(object:object, name_method:str, *args)->Callable:
        call_method = getattr(object, name_method)
        return call_method
    
    @staticmethod
    def get_function_info_v1(fn:Callable[..., Any], *args, **kwargs)->dict:
            fn_datas:dict = {}
            fn_args:list[dict] = []

            fn_datas['args'] = args
            fn_datas['kwargs'] = kwargs
            fn_datas['class'] = inspect._findclass(fn)
            fn_datas['name'] = fn.__name__
            fn_datas['type'] = type(fn_datas['class'].__dict__[fn.__name__])
            fn_datas['type_method'] = ExtReflection.get_type_method(fn)
            fn_datas['return_type'] = fn.__annotations__['return'] if 'return' in fn.__annotations__ else None

            fn_params = inspect.signature(fn)
            for index, param_name in enumerate(fn_params.parameters):
                param_d = fn_params.parameters[param_name]
                type_param = param_d.annotation if not param_d.annotation is inspect._empty else inspect._empty
                fn_args.append({'arg_pos': index, 'name': param_name, 'type': type_param})

                if param_d.default != inspect.Parameter.empty:
                    fn_args[index]['default'] = param_d.default

            fn_datas['params'] = fn_args

            return fn_datas

    @staticmethod
    def init_inject(func: _C)-> _C:

        @wraps(func)
        def wrapper(*args, **kwargs)->Any:
            if 'is_inject' not in kwargs:
                fn_datas = ExtReflection.get_function_info_v1(func)
                new_args = list(args)

                for item in fn_datas['params']:
                    if item['name'] != 'self':
                        check_type = item['type']
                        if ResolveProviderFWDI.contains(check_type):    #issubclass(check_type, BaseServiceFWDI):
                            search_service = ResolveProviderFWDI.get_service(item['type'])
                            if search_service != None:
                                new_args.append(search_service)

                result = func(*new_args, **kwargs)
                return result
            else:
                new_args = {}
                for item in [item for item in kwargs if item != 'is_inject']:
                    element = {item:kwargs[item]}
                    new_args.update(element)

                result = func(*args, **new_args)
                return result

        return wrapper
    
    @staticmethod
    def __get_default(lst_sign:list[inspect.Parameter], name_key:str) -> Any:
        search = [item for item in lst_sign if item.name == name_key]
        if len(search) > 0:
            search_value = search[0]
            if not search_value.default is inspect._empty:
                return search_value.default
        
        return None
    
    @staticmethod
    def get_function_info_v2(fn:Callable[..., Any], args:tuple, kwargs:dict)->dict:
            fn_datas:dict = {}
            fn_args:list[dict] = []

            fn_datas['method_class'] = inspect._findclass(fn)
            fn_datas['method_name'] = fn.__name__

            fn_datas['type'] = type(fn)
            fn_datas['method_type'] = ExtReflection.get_type_method(fn)
            fn_datas['method_signature'] = list(inspect.signature(fn.__wrapped__ if hasattr(fn, '__wrapped__') else fn).parameters.values())
            fn_datas['has_self'] = True if len([item for item in fn_datas['method_signature'] if item.name == 'self']) > 0 else False
            fn_datas['coroutine'] = inspect.iscoroutinefunction(fn)
            fn_datas['origin_args'] = args
            fn_datas['origin_kwargs'] = kwargs

            _arg_has_self_ = False if len(args) == 0 else True if type(args[0]) == fn_datas['method_class'] else False
            if _arg_has_self_ and fn_datas['has_self']:
                fn_datas['method_signature'] = fn_datas['method_signature'][1:]
            elif _arg_has_self_ and not fn_datas['has_self']:
                fn_datas['origin_args'] = args[1:]
            elif not _arg_has_self_ and fn_datas['has_self']:
                raise Exception(f'Error no self in args! :: {fn.__module__}:{fn}')
                
            fn_datas['is_object_call'] = True if fn_datas['has_self'] and _arg_has_self_ else False

            if fn_datas['method_name'] in fn_datas['method_class'].__dict__:
                _annotations = fn_datas['method_class'].__dict__[fn_datas['method_name']].__annotations__
            else:
                _annotations = fn.__annotations__
            fn_datas['method_return'] = _annotations['return'] if 'return' in _annotations else None

            without_return = [item for item in _annotations if item != 'return']
            for param_name in without_return:
                type_param = _annotations[param_name]
                default_param = ExtReflection.__get_default(fn_datas['method_signature'], param_name)
                fn_args.append({'name': param_name, 'type': type_param, 'default':default_param})

            fn_datas['method_params'] = fn_args
            
            if not fn_datas['has_self'] and len(fn_datas['method_signature']) != len(fn_datas['method_params']) and len(fn_datas['origin_args']) == 0:
                raise Exception(f"Error length __annotations__ Not Equal signature::{fn.__module}:{fn}")

            if len(fn_datas['method_signature']) != len(fn_datas['method_params']) and len(fn_datas['origin_args']) == 0:
                raise Exception(f"Error length __annotations__ Not Equal signature::{fn.__module}:{fn}")

            return fn_datas

    @staticmethod
    def get_new_arguments(info_method_args:dict)->dict:
        args = info_method_args['args']
        kwargs = info_method_args['kwargs']

        find_args:list[dict] = [item for item in info_method_args['params'] if item['name'] != 'self']
        
        new_kwargs_params:dict[str, any] = {}
        if Utilities.search_key(info_method_args['params'], 'self'):
            new_kwargs_params['self'] = args[0]
        else:
            #if not Utilities.search_key(info_method_args['params'], 'self'):
            if len(args) > 1:
                if type(args[0]) is not info_method_args['class']:
                    new_kwargs_params[find_args[0]['name']] = args[0]
                    find_args = find_args[1:]
                else:
                    new_kwargs_params[find_args[0]['name']] = args[1]
                    find_args = find_args[2:]
            """
            else:
                if len(kwargs) == 0:
                    find_args = find_args[1:]

                if len(args) > 0:
                    new_kwargs_params[find_args[0]['name']] = args[0]
                    find_args = find_args[1:]
            """
        
        count_args = len(args)
        for item in find_args:
            arg_pos, arg_name, arg_type = item['arg_pos'], item['name'], item['type']
            if count_args >= 1:
                if arg_pos < count_args:
                    arg_item = args[arg_pos]

                    if type(arg_item) == arg_type:
                        new_kwargs_params[arg_name] = args[arg_pos]
                    elif type(arg_item) is list:
                        new_kwargs_params[arg_name] = args[arg_pos]
                    else:
                        if len(kwargs) > 0:
                            try_get_value = kwargs.get(arg_name)
                            if try_get_value != None:
                                new_kwargs_params[arg_name] = try_get_value
                        else:
                            if ResolveProviderFWDI.contains(arg_type):#issubclass(arg_type, BaseServiceFWDI):
                                new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)
                else:

                    if ResolveProviderFWDI.contains(arg_type):
                        new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)
                    else:
                        if len(kwargs) > 0:
                            try_get_value = kwargs.get(arg_name)
                            new_kwargs_params[arg_name] = try_get_value if try_get_value != None else ResolveProviderFWDI.get_service(arg_type)
                        else:
                            if ResolveProviderFWDI.contains(arg_type):
                                new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)
                            elif ResolveProviderFWDI.contains(arg_type):
                                new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)
                            elif 'default' in item:
                                new_kwargs_params[arg_name] = item['default']

            else:
                if len(kwargs) > 0:
                    try_get_value = kwargs.get(arg_name)
                    if try_get_value != None:
                        new_kwargs_params[arg_name] = try_get_value
                    else:
                        if ResolveProviderFWDI.contains(arg_type):
                            new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)
                else:
                    if ResolveProviderFWDI.contains(arg_type):
                        new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)

        return new_kwargs_params

    @staticmethod
    def __static_gen_new_args(info:dict)->dict:
        kwargs = info['origin_kwargs']
        find_args:list[dict] = info['method_params']
        len_args = len(info['origin_args'])
        
        new_kwargs_params:dict[str, any] = {}

        if len_args > 0:
            find_args = find_args[len_args:]

        for item in find_args:
            arg_name, arg_type = item['name'], item['type']
            if arg_name in kwargs:
                try_get_value = kwargs.get(arg_name)
                new_kwargs_params[arg_name] = try_get_value
            else:
                if ResolveProviderFWDI.contains(arg_type):
                    new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)
                elif 'default' in item and item['default'] != None:
                    new_kwargs_params[arg_name] = item['default']
                elif ResolveProviderFWDI.contains(arg_type):
                    new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)

        return new_kwargs_params

    @staticmethod
    def __instance_gen_new_args(info:dict)->dict:
        args:tuple = info['origin_args']
        kwargs:dict = info['origin_kwargs']
        signature:list[dict] = info['method_signature'] 
        method_params:list[dict] = info['method_params']

        new_kwargs_params:dict[str, any] = {}
        len_args:int = len(args)

        if len_args > 1:
            shift_args = len_args - 1
            method_params = method_params[shift_args:]

        for item in method_params:
            arg_name, arg_type = item['name'], item['type']
            if len(kwargs) > 0:
                if arg_name in kwargs:
                    try_get_value = kwargs.get(arg_name)
                    new_kwargs_params[arg_name] = try_get_value
                else:
                    if ResolveProviderFWDI.contains(arg_type):
                        new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)
            else:
                if ResolveProviderFWDI.contains(arg_type):
                    new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)
                elif ResolveProviderFWDI.contains(arg_type):
                    new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)
                elif 'default' in item:
                    new_kwargs_params[arg_name] = item['default']

        return new_kwargs_params

    @staticmethod
    def __classmethod_gen_new_args(info:dict)->dict:

        args:tuple = info['origin_args']
        kwargs:dict = info['origin_kwargs']
        signature:list[dict] = info['method_signature'] 
        method_params:list[dict] = info['method_params']

        new_kwargs_params:dict[str, any] = {}
        len_args:int = len(args)

        if len_args > 1:
            shift_args = len_args - 1
            method_params = method_params[shift_args:]

        for item in method_params:
            arg_name, arg_type = item['name'], item['type']
            if len(kwargs) > 0:
                if arg_name in kwargs:
                    try_get_value = kwargs.get(arg_name)
                    new_kwargs_params[arg_name] = try_get_value
                else:
                    if ResolveProviderFWDI.contains(arg_type):
                        new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)
            else:
                if ResolveProviderFWDI.contains(arg_type):
                    new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)
                elif ResolveProviderFWDI.contains(arg_type):
                    new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)
                elif 'default' in item:
                    new_kwargs_params[arg_name] = item['default']

        return new_kwargs_params

    @staticmethod
    def _log_inject(func: _C) -> _C:

        @wraps(func)
        def __sync(*args, **kwargs)->_C:
            if GlobalSettingService.log_lvl == TypeLoggingLevel.DEBUG or GlobalSettingService.log_lvl == TypeLoggingLevel.ALL:
                ExtReflection.__log__(f"sync exec :{func.__module__}::{func.__name__}", 'debug')
            try:
                t_start = time.perf_counter_ns()

                result_call = func(*args, **kwargs)
                
                if GlobalSettingService.log_lvl == TypeLoggingLevel.DEBUG or GlobalSettingService.log_lvl == TypeLoggingLevel.ALL:
                    time_call = time.perf_counter_ns() - t_start
                    ExtReflection.__log__(f"run: {args} = duration time :{func.__name__}={time_call}")

                return result_call
            except Exception as ex:
                ExtReflection.__log__(f"error exec :{func.__name__} Error:{ex}::{args}, {kwargs}", 'error')
                return None
    
        @wraps(func)
        async def __async(*args, **kwargs)->_C:
            if GlobalSettingService.log_lvl == TypeLoggingLevel.DEBUG or GlobalSettingService.log_lvl == TypeLoggingLevel.ALL:
                ExtReflection.__log__(f"sync exec :{func.__module__}::{func.__name__}")
            try:
                t_start = time.perf_counter_ns()
                
                result_call = await func(*args, **kwargs)
                
                if GlobalSettingService.log_lvl == TypeLoggingLevel.DEBUG or GlobalSettingService.log_lvl == TypeLoggingLevel.ALL:
                    time_call = time.perf_counter_ns() - t_start
                    ExtReflection.__log__(f"    duration time :{func.__name__}={time_call}")

                return result_call
            except Exception as ex:
                ExtReflection.__log__(f"error exec :{func.__name__}\n Error:{ex}\n{args}, {kwargs}", 'error')
                return None

        
        return __async if inspect.iscoroutinefunction(func) else __sync

    @_log_inject
    @staticmethod
    def _inject_(func: _C)->_C:
        ExtReflection.count_inject += 1
        
        @wraps(func, updated=())
        def __sync(*args, **kwargs)->_C:
            if not ResolveProviderFWDI.is_init():
                return func(*args, **kwargs)
            
            if 'is_inject' not in kwargs:
                method_info = ExtReflection.get_function_info_v2(func, args, kwargs)
                args = method_info['origin_args']
                kwargs = method_info['origin_kwargs']
                length_param = len(method_info['method_params'])
                len_args = len(args)
                new_args:dict = {}

                if not method_info['has_self'] and len_args == length_param:
                    result = func(*args, **kwargs)
                    return result
                elif method_info['has_self'] and (len_args - 1) == length_param:
                    result = func(*args, **kwargs)
                    return result
                elif method_info['has_self'] and len_args == 1 and length_param == 0:
                    result = func(*args, **kwargs)
                    return result

                match method_info['method_type']:
                    case TypeMethod.Instance:
                        new_args = ExtReflection.__instance_gen_new_args(method_info)
                    case TypeMethod.Static:
                        if method_info['has_self']:
                            new_args = ExtReflection.__instance_gen_new_args(method_info)
                        else:
                            new_args = ExtReflection.__static_gen_new_args(method_info)
                    case TypeMethod.Classmethod:
                        new_args = ExtReflection.__classmethod_gen_new_args(method_info)
                
                result = func(*args, **new_args)
                return result
            else:
                new_args = [item for item in kwargs if item != 'is_inject']
                result = func(*args, **new_args)

            return result

        @staticmethod
        @wraps(func)
        async def __async(*args, **kwargs)->_C:
            if not ResolveProviderFWDI.is_init():
                return await func

            if 'is_inject' not in kwargs:
                method_info = ExtReflection.get_function_info_v2(func, args, kwargs)
                args = method_info['origin_args']
                kwargs = method_info['origin_kwargs']
                length_param = len(method_info['method_params'])
                len_args = len(args)
                new_args:dict = {}

                if len(kwargs) > 0 and len_args == length_param:
                    result = func(*args, **kwargs)
                    return result
                
                if not method_info['has_self'] and len_args == length_param:
                    result = func(*args, **kwargs)
                    return result
                elif method_info['has_self'] and (len_args - 1) == length_param:
                    result = func(*args, **kwargs)
                    return result
                elif method_info['has_self'] and len_args == 1 and length_param == 0:
                    result = func(*args, **kwargs)
                    return result

                match method_info['method_type']:
                    case TypeMethod.Instance:
                        new_args = ExtReflection.__instance_gen_new_args(method_info)
                    case TypeMethod.Static:
                        if method_info['has_self']:
                            new_args = ExtReflection.__instance_gen_new_args(method_info)
                        else:
                            new_args = ExtReflection.__static_gen_new_args(method_info)
                    case TypeMethod.Classmethod:
                        new_args = ExtReflection.__classmethod_gen_new_args(method_info)
                
                result = await func(*args, **new_args)

                return result
            else:
                new_args = [item for item in kwargs if item != 'is_inject']
                result = await func(*args, **new_args)

            return result
        
        return __async if inspect.iscoroutinefunction(func) else __sync
    
    @staticmethod
    def is_class(obj)->bool:
        return True if isinstance(obj, type) else False
    
    @staticmethod
    def is_injectable_init(obj)->bool:
        return True if '__init__' in obj.__dict__ else False