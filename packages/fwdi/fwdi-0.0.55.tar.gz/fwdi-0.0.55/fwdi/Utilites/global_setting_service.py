
from enum import Enum


class TypeLoggingLevel(Enum):
    INFO = 0,
    DEBUG=1,
    ALL=2,

class GlobalSettingService():
    log_lvl:TypeLoggingLevel = TypeLoggingLevel.INFO