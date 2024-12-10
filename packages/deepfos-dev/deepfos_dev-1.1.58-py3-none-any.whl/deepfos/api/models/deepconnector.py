from typing import Optional, Dict

from .base import BaseModel

__all__ = [
    "ConnectionInfoVo"
]


class ConnectionInfoVo(BaseModel):
    authMethod: Optional[str]
    connectionHost: str
    connectionPort: int
    dbName: str
    elementName: Optional[str]
    encryption: bool
    extraParam: Optional[str]
    folderId: str
    folderPath: str
    i18nName: Optional[Dict[str, str]]
    id: str
    password: str
    serviceCode: Optional[str]
    serviceName: str
    serviceType: Optional[int]
    serviceTypeName: Optional[str]
    serviceVersion: Optional[str]
    username: str
