from .jwt_tools import JwtToolsFWDI
from ..Application.Abstractions.base_service_collection import BaseServiceCollectionFWDI

class DependencyInjection():

    @staticmethod
    def AddUtilites(services:BaseServiceCollectionFWDI)->None:
        services.AddTransient(JwtToolsFWDI)