from enum import Enum


class NotifyTypeEnum(str, Enum):
    APP = "app"
    LINE = "line"
    SMS = "sms"
    NOTIFICATION = "notification"
    WEBSOCKET = "websocket"
