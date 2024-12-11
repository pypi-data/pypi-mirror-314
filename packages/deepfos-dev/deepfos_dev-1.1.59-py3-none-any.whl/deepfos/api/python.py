from .base import DynamicRootAPI, ChildAPI, get, post
from .models.python import *
from deepfos.lib.decorator import cached_property
from typing import List, Dict, Union, Any, Awaitable


class WorkerAPI(ChildAPI):
    endpoint = '/worker'

    @post('register')
    def register(self, worker_info: WorkerRegistry) -> Union[bool, Awaitable[bool]]:
        return {'body': worker_info}

    @get('metrics')
    def metrics(self, ) -> Union[List[WorkerMetrics], Awaitable[List[WorkerMetrics]]]:
        return {}


class ScriptAPI(ChildAPI):
    endpoint = '/script'

    @post('run')
    def run(self, run_info: PyRunInfo) -> Union[str, Awaitable[str]]:
        return {'body': run_info}

    @get('result')
    def result(self, task_id: str, timeout: int = None) -> Union[Any, Awaitable[Any]]:
        return {'param': {'timeout': timeout}, 'path': task_id}

    @post('terminate')
    def terminate(self, task_id: str) -> Union[Any, Awaitable[Any]]:
        return {'body': {"taskId": task_id}}


class FileAPI(ChildAPI):
    endpoint = '/file'

    @post('add')
    def add(self, file: PyNewFile) -> Union[bool, Awaitable[bool]]:
        """
        新建python文件

        """
        return {'body': file}

    @post('update')
    def update(self, file: PyNewFile) -> Union[bool, Awaitable[bool]]:
        """
        更新文件内容

        """
        return {'body': file}

    @get('read')
    def read(self, info: PyBaseInfo) -> Union[PyNewFileWithError, Awaitable[PyNewFileWithError]]:
        """
        读取文件内容

        """
        return {'param': info}


class PythonAPI(DynamicRootAPI, builtin=True):
    module_type = 'PY'
    default_version = (2, 0)
    multi_version = False
    cls_name = 'PythonAPI'
    module_name = 'deepfos.api.python'
    api_version = (2, 0)

    @cached_property
    def worker(self) -> WorkerAPI:
        return WorkerAPI(self)

    @cached_property
    def script(self) -> ScriptAPI:
        return ScriptAPI(self)

    @cached_property
    def file(self) -> FileAPI:
        """
        python文件管理相关接口
        """
        return FileAPI(self)
