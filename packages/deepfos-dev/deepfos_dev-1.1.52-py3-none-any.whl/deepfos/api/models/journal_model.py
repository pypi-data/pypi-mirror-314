"""
Models used by /journal-model-server1-0
"""

from deepfos.api.models.base import BaseModel
from typing import List, Optional, Any, Dict

__all__ = [
    'CheckStandardDataVO',
    'CheckStandardVO',
    'ColumnAliasDTO',
    'ElementDetailDTO',
    'MessageDTO',
    'ModelDataColumnDTO',
    'ModelDataQueryVO',
    'QueryWhereDTO',
    'JmPostParamVO',
    'JmPostResultVO',
    'JournalModelExecCallbackPythonDTO',
    'CommonResultDTO',
    'ModelDataBatchDTO',
    'ModelDataDeleteDTO',
    'ModelDataDTO',
    'JournalModelConfig',
    'ModelColumnVO',
    'ModelDataTableVO',
    'ModelTableVO',
    'JournalModelTypeVo',
    'JournalSortConfig'
]


class ElementDetailDTO(BaseModel):
    #: 是否绝对路径
    absoluteTag: Optional[bool]
    #: 多语言
    description: Optional[Any]
    #: 元素名称
    elementName: Optional[str]
    #: 元素类型
    elementType: Optional[str]
    #: 目录id
    folderId: Optional[str]
    #: 多语言使用的key
    languageKey: Optional[str]
    #: 元素对应组件版本
    moduleVersion: Optional[str]
    #: 元素绝对路径
    path: Optional[str]
    #: 元素相对路径
    relativePath: Optional[str]
    #: 组件id
    serverName: Optional[str]
    #: 凭证类型代码
    vmTypeCode: Optional[str]


class ModelColumnVO(BaseModel):
    name: Optional[str]
    operation: Optional[str]


class ModelDataTableVO(BaseModel):
    id: Optional[str]
    #: 元素编码
    name: Optional[str]
    #: 真实表名
    actualTableName: Optional[str]
    #: 文件夹ID
    folderId: Optional[str]
    #: 元素详细信息
    elementDetail: Optional[ElementDetailDTO]
    #: 子表
    children: Optional[List[Any]]


class ModelTableVO(BaseModel):
    #: 表的uuid
    tableUuid: Optional[str]
    #: 父表的uuid
    parentUuid: Optional[str]
    #: 数据表信息
    dataTableInfo: Optional[ModelDataTableVO]
    #: 字段列集合
    columns: Optional[List[ModelColumnVO]]
    #: 子表集合
    children: Optional[List['ModelTableVO']]


class JournalModelTypeVo(BaseModel):
    #: 凭证Tag
    journalTag: Optional[str]
    #: 凭证类型代码
    typeCode: Optional[str]


class JournalModelConfig(BaseModel):
    #: 逻辑表信息
    logicTable: Optional[ModelTableVO]
    #: 层级，0为顶层
    level: Optional[int]
    #:
    type: Optional[str]
    #: 凭证基础信息
    baseInfo: Optional[Any]
    #: 凭证自定义逻辑
    customLogic: Optional[Any]
    #: 报错集合
    errorList: Optional[Any]
    #: 警告集合
    warningList: Optional[Any]
    #: 凭证类型集合
    journalModelType: Optional[List[JournalModelTypeVo]]


class CheckStandardDataVO(BaseModel):
    #: mainId
    mainId: Optional[str]
    #: 凭证id
    journalId: Optional[str]
    #: 凭证类型代码
    journalTypeCode: Optional[str]


class CheckStandardVO(BaseModel):
    #: 凭证id和凭证类型代码集合
    dataList: Optional[List[CheckStandardDataVO]]
    #: 凭证模型名称
    elementName: Optional[str]
    #: 凭证模型文件夹ID
    folderId: Optional[str]
    #: 凭证模型路径
    path: Optional[str]
    # 筛选条件
    whereStr: Optional[str]


class ColumnAliasDTO(BaseModel):
    #: field
    field: Optional[str]
    #: id
    id: Optional[str]
    #: sort
    sort: Optional[str]
    #: viewKey
    viewKey: Optional[str]


class MessageDTO(BaseModel):
    #: 别名
    alias: Optional[ColumnAliasDTO]
    #: 描述
    description: Optional[str]
    #: msg
    msg: Optional[str]
    #: title
    title: Optional[str]


class ModelDataColumnDTO(BaseModel):
    #: 权限值
    accessRight: Optional[int]
    #: 字段别名,用于定位字段在明细表中位置
    alias: Optional[ColumnAliasDTO]
    #: 字段名
    columnName: Optional[str]
    #: 原始字段值
    oldValue: Optional[Any]
    #: 操作类型
    operateType: Optional[str]
    #: 字段值
    value: Optional[Any]


class JournalSortConfig(BaseModel):
    #: 字段名
    col: Optional[str]
    #: 排序类型 ：ASC 或 DESC, 默认为 ASC
    type: Optional[str]


class ModelDataQueryVO(BaseModel):
    #: 数据表目录id
    dataTableFolderId: Optional[str]
    #: 数据表名称(从该数据表开始查,此时对应mainKeys为该表业务主键)
    dataTableName: Optional[str]
    #: 数据表目录(与dataTableFolderId传一个即可)
    dataTablePath: Optional[str]
    #: 凭证模型名称
    elementName: Optional[str]
    #: 返回结果中排除指定表的目录id
    excludeDataTableFolderId: Optional[str]
    #: 返回结果中排除指定表的表名(返回结果中排除指定表下子表的数据)
    excludeDataTableName: Optional[str]
    #: 返回结果中排除指定表的目录
    excludeDataTablePath: Optional[str]
    #: 凭证模型所在目录id(与path传一个即可)
    folderId: Optional[str]
    #: 返回结果中是否包含字段权限信息 默认值:false
    includeAccess: Optional[bool]
    #: 凭证模型主表（或传入表）的业务主键的值集合
    mainKeys: Optional[List[Dict]]
    #: 凭证模型所在路径
    path: Optional[str]
    #: 数据查询时的where条件
    whereStr: Optional[str]
    #: 返回的头表列名 集合，不指定，则取头表所有字段
    headQueryCols: Optional[List[str]]
    #: 返回的行表列名 集合，不指定，则取行表所有字段
    lineQueryCols: Optional[List[str]]
    #: 返回的列名 集合
    sortConfig: Optional[List[JournalSortConfig]]



class QueryWhereDTO(BaseModel):
    #: 字段名
    columnName: Optional[str]
    #: 操作符
    operationCode: Optional[str]
    #: 字段值
    value: Optional[Any]


class JmPostParamVO(BaseModel):
    #: 需过账|取消过账数据ID集合
    dataIds: Optional[List[str]]
    #: 凭证模型名称
    elementName: Optional[str]
    #: 凭证模型文件夹ID
    folderId: Optional[str]
    #: 凭证模型路径
    path: Optional[str]
    #: 筛选条件
    whereStr: Optional[str]


class JmPostResultVO(BaseModel):
    #: fmPostMsg
    fmPostMsg: Optional[Any]
    #: msg
    msg: Optional[str]
    #: 过账结果
    postResult: Optional[Any]
    #: success
    success: Optional[bool]


class JournalModelExecCallbackPythonDTO(BaseModel):
    #: PY所在路径，与folderId二选一
    path: Optional[str]
    #: PY所在文件夹ID，与path二选一
    folderId: Optional[str]
    #: PY的元素名称
    elementName: str
    #: 类型 默认值 PY
    elementType: Optional[str]
    #: Python服务名，如：python-server2-0
    serverName: Optional[str]
    #: 传给回调的参数，{key1:value1,key2:value2}
    callbackParams: Optional[Dict]


class CommonResultDTO(BaseModel):
    #: errors
    errors: Optional[List[MessageDTO]]
    #: success
    success: Optional[bool] = True
    #: warnings
    warnings: Optional[List[MessageDTO]]
    # infos
    infos: Optional[List[MessageDTO]]
    # successInfo
    successInfo: Optional[List[MessageDTO]]
    #: error_refresh
    errorRefresh: Optional[bool]
    # 业务主键
    mainKey: Optional[Dict]


class ModelDataBatchDTO(BaseModel):
    #: 数据集合
    dataMap: Optional[Any]
    #: 是否启用创建人、创建时间自动赋值，默认为True
    enableCreate: Optional[bool]
    #: 是否启用字段值为空时使用默认值填充，默认为False
    enableDefaultValue: Optional[bool]
    #: 是否启用业务主键重复的校验，默认为True
    enableRepeatCheck: Optional[bool]
    #: 是否启用必填字段的校验，默认为False
    enableRequired: Optional[bool]
    #: 是否启用有效性范围的校验，默认为True
    enableValidRange: Optional[bool]
    #: 是否启用一次性校验所有规则和数据，默认为True
    enableAllErrors: Optional[bool]
    #: 是否启用凭证行表至少需要一条数据的校验，默认为True
    enableNeedOneLine: Optional[bool]
    #: modelInfo
    modelInfo: Optional[ElementDetailDTO]
    #: 执行参数值列表{key1:value1,key2:value2}
    paramValueMap: Optional[Any]
    #: 回调信息
    callbackInfo: Optional[JournalModelExecCallbackPythonDTO]


class ModelDataDeleteDTO(BaseModel):
    #: 元素名
    elementName: Optional[str]
    #: 所属目录id
    folderId: Optional[str]
    #: 业务字段数据集合
    mainKeyList: Optional[List[Dict]]
    #: 子模型分区ID
    partitionId: Optional[str]
    #: 所属目录
    path: Optional[str]
    #: 数据删除时的where条件
    whereList: Optional[List[QueryWhereDTO]]
    #: 数据删除时的where条件
    whereStr:  Optional[str]



class ModelDataDTO(BaseModel):
    #: 子数据信息
    children: Optional[List['ModelDataDTO']]
    #: 数据表字段及值
    columns: Optional[List[ModelDataColumnDTO]]
    #: 数据表目录编码
    dataTableFolderId: Optional[str]
    #: 数据表名（元素名）
    dataTableName: Optional[str]
    #: 数据表目录
    dataTablePath: Optional[str]
    #: mainId
    mainId: Optional[str]



ModelTableVO.update_forward_refs()
ModelDataDTO.update_forward_refs()
