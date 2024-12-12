from abc import ABCMeta, abstractmethod
from pydantic import BaseModel

class BaseRestClientFWDI(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def IsAuth(self):
        ...

    @abstractmethod
    def login(self, url:str='/token')->bool:
        ...
    
    @abstractmethod
    def get(self, path:str, _data:BaseModel)->any:
        ...

    @abstractmethod
    def post(self, path:str, _data:BaseModel)->any:
        ...