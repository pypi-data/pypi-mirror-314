from typing import Union, Awaitable

from deepfos.element.base import T_ElementInfoWithServer
from deepfos.lib.decorator import cached_property

from .base import ChildAPI, get, RootAPI
from .models.deepconnector import *


class DataSourceAPI(ChildAPI):
    endpoint = '/apis/v3/ds/spaces/{space}/apps/{app}'

    @get('connection-info', data_wrapped=False)
    def connection_info(self, element_info: T_ElementInfoWithServer) -> Union[ConnectionInfoVo, Awaitable[ConnectionInfoVo]]:
        return {
            'param': {
                'elementName': element_info.elementName,
                'folderId': element_info.folderId
            }
        }


class DeepConnectorAPI(RootAPI):
    prefix = lambda: 'http://deep-connector-server'
    url_need_format = True
    module_type = 'CONN'

    @cached_property
    def datasource(self) -> DataSourceAPI:
        return DataSourceAPI(self)
