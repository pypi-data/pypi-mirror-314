import base64

from deepfos.api.deepconnector import DeepConnectorAPI
from deepfos.api.models import BaseModel
from deepfos.element.base import ElementBase, SyncMeta
from deepfos.lib.asynchronous import future_property
from deepfos.lib.decorator import cached_property

__all__ = ['AsyncDeepConnector', 'DeepConnector', 'ConnectionInfo']


class ConnectionInfo(BaseModel):
    host: str
    port: int
    db: str
    user: str
    password: str
    dbtype: str


# -----------------------------------------------------------------------------
# core
class AsyncDeepConnector(ElementBase[DeepConnectorAPI]):
    """连接器"""

    @cached_property
    def api(self):
        """同步API对象"""
        api = self.api_class(sync=True)
        return api

    @future_property
    async def async_api(self):
        """异步API对象"""
        return await self._init_api()

    async def _init_api(self):
        return self.api_class(sync=False)

    @future_property
    async def connection_info(self) -> ConnectionInfo:
        """当前连接器元素的连接信息"""
        api = await self.wait_for('async_api')
        ele_info = await self.wait_for('element_info')
        info = await api.datasource.connection_info(
            element_info=ele_info,
        )
        return ConnectionInfo(
            host=info.connectionHost,
            port=info.connectionPort,
            db=info.dbName,
            user=info.username,
            password=base64.decodebytes(info.password.encode()).decode(),
            dbtype=info.serviceName,
        )


class DeepConnector(AsyncDeepConnector, metaclass=SyncMeta):
    pass
