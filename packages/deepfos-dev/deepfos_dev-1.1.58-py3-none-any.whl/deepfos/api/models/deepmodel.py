from typing import List, Optional, Dict, Any

from pydantic import Field

from .base import BaseModel

__all__ = [
    "ObjectBasicDTO",
    "ObjectInfo",
    "ObjectLinkParam",
    "ObjectPropertyParamRes",
    "ObjectParam",
    "ObjectOperationParam",
    "QueryResult",
    "QueryResultObjectInfo",
    "FieldInfo",
    "ParamElement",
    "RuleInfoRes",
    "RuleErrorMsg",
    "RuleParam",
    "SequenceInstance",
    "_IndexParam",
    "SimpleSpaceConnectionConfig",
    "QlGlobalVariableVO",
    "QlRecordVO"
]


class ObjectBasicDTO(BaseModel):
    #: 对象所属应用
    app: Optional[str]
    #: 对象所属应用名称
    appName: Optional[str]
    #: 对象编码
    code: Optional[str]
    #: 对象名称
    name: Optional[Dict[str, Optional[str]]]
    #: 对象范围 1：应用级对象 2：空间级对象
    objectScope: Optional[int]


class ObjectInfo(BaseModel):
    #: 链接目标对象所在应用id,如果传过来的是_system代表链接的是空间级对象
    app: Optional[str]
    #: 链接目标对象所在应用名称
    appName: Optional[str]
    #: 链接对象的编码
    code: Optional[str]
    #: 引用对象当前语种名称
    objectName: Optional[str]
    #: 是否为引用对象的链接
    whetherQuotedRelation: Optional[bool]
    #: 是否是为对象指向的链接
    whetherSelfRelation: Optional[bool]


class ObjectLinkParam(BaseModel):
    app: Optional[str]
    code: Optional[str]
    currentObjectUnique: Optional[bool]
    deleteCategory: Optional[str]
    inferBase: Optional[str]
    inferType: Optional[str]
    linkId: Optional[str]
    linkObjectOption: Optional[int]
    linkObjectRequired: Optional[bool]
    linkType: Optional[int]
    name: Optional[Dict[str, Optional[str]]]
    sourceObjectCode: Optional[str]
    state: Optional[int]
    targetApp: Optional[str]
    targetObject: Optional['ObjectParam']
    targetObjectCode: Optional[str]
    targetObjectInfo: Optional[ObjectInfo]
    whetherSystem: Optional[bool]


class ObjectPropertyParamRes(BaseModel):
    #: 应用id
    app: Optional[str]
    #: 是否自动赋值
    autoValue: Optional[bool]
    #: 属性编码
    code: str
    #: 约束
    constraint: Optional[str]
    #: 默认值 默认值类型（0 无,1 定值，2 当前时间 3 枚举）
    defaultValue: Optional[str]
    #: 默认值类型 默认值类型（0 无,1 定值）
    defaultValueType: Optional[int]
    #: 推断基数: AT_LEAST_ONE, AT_MOST_ONE, MANY, ONE
    inferBase: Optional[str]
    #: 最大长度
    maxLength: Optional[int]
    #: 最大数量
    maxNum: Optional[int]
    #: 最大值
    maxValue: Optional[str]
    #: 最大值条件，枚举值 LESS_OR_EQUALS 小于等于；LESS 小于
    maxValueCondition: Optional[str]
    #: 最小值
    minValue: Optional[str]
    #: 最小值条件 GREATER_OR_EQUALS 大于等于；GREATER大于
    minValueCondition: Optional[str]
    #: 属性名称
    name: Dict[str, Optional[str]]
    #: 对象编码
    objectCode: Optional[str]
    #: 是否是业务主键
    whetherBusinessKey: bool
    #: 是否是计算属性
    whetherCalculation: bool
    #: 是否唯一
    whetherOnly: bool
    #: 是否只读
    whetherReadOnly: bool
    #: 是否必填
    whetherRequired: bool
    #: 是否系统属性
    whetherSystemProperties: bool
    propertyId: Optional[str]


class _IndexParam(BaseModel):
    objectIndexId: Optional[str]
    objectCode: Optional[str]
    indexType: Optional[str]
    indexFieldList: Optional[List[str]]
    indexFieldIdList: Optional[List[str]]


class ObjectParam(BaseModel):
    app: Optional[str]
    appName: Optional[str]
    code: Optional[str]
    linkCodes: Optional[List[str]]
    linkParamList: Optional[List[ObjectLinkParam]]
    name: Optional[Dict[str, Optional[str]]]
    objectId: Optional[str]
    objectScope: Optional[int]
    objectTypeList: Optional[List[str]]
    propertyCodes: Optional[List[str]]
    propertyParamList: Optional[List[ObjectPropertyParamRes]]
    selfLinkOrder: Optional[int]
    state: Optional[int]
    #: 对象类型: BUILTIN, STANDARD, VIEW
    type: Optional[str]
    whetherSelfReference: Optional[bool]
    businessKey: Optional[str]
    indexParamList: Optional[List[_IndexParam]]
    unitedOnlyList: Optional[List[_IndexParam]]


class ObjectOperationParam(BaseModel):
    objectList: List[ObjectParam]


class FieldInfo(BaseModel):
    name: str
    type: str
    fields: Optional[List]


class QueryResultObjectInfo(BaseModel):
    objectKey: str
    fields: List[FieldInfo]


class QueryResult(BaseModel):
    objectInfos: Optional[List[QueryResultObjectInfo]]
    json_: Any = Field(alias='json')


class RuleErrorMsg(BaseModel):
    errorCode: Optional[str]
    errorMessage: Optional[str]
    fieldTip: Optional[str]
    fieldName: Optional[List[Any]]


class ParamElement(BaseModel):
    # 规则参数类型为SEQUENCE时使用
    sequenceCode: Optional[str]
    # 规则参数类型为SEQUENCE时使用
    sequenceKeyType: Optional[str]
    # 规则参数类型为SEQUENCE时使用
    valueFormat: Optional[str]
    # 规则参数类型为SEQUENCE时使用
    sequenceId: Optional[str]
    # 规则参数类型为RANDOM_CHARACTER/SEQUENCE时使用
    length: Optional[int]
    # 规则参数类型为CURRENT_TIME时使用
    dateFormat: Optional[str]
    # 规则参数类型为OBJECT_PROPERTY时使用
    propertyLinkId: Optional[str]
    # 规则参数类型为OBJECT_PROPERTY时使用
    propertyLinkCode: Optional[str]


class RuleParam(BaseModel):
    #: 规则名称
    code: str
    #: 规则参数编号
    id: Optional[str]
    #: 规则标识
    key: Optional[str]
    #: 参数内容
    paramContent: Optional[ParamElement]
    #: 参数内容 json
    paramContentJson: Optional[str]
    #: 规则编号
    ruleId: Optional[str]
    #: 规则参数类型 [ "CURRENT_TIME", "OBJECT_PROPERTY", "RANDOM_CHARACTER", "SEQUENCE"]
    ruleParamType: str
    #: 排序
    sort: Optional[int]


class RuleInfoRes(BaseModel):
    #: 规则名称
    code: str
    #: 启用状态
    enable: Optional[bool]
    #: 执行条件,可用值:ALWAYS_EXECUTE,NULL_EXECUTE
    executeCondition: Optional[str]
    #: 规则编号
    id: Optional[str]
    #: 规则所属对象id
    objectCode: str
    #: 赋值属性
    propertyCode: Optional[str]
    #: 赋值属性id
    propertyId: Optional[str]
    #: 规则类型 [SYSTEM_RULE-系统规则、TEXT_PROPERTY_ASSIGNMENT-文本属性赋值]
    ruleType: str
    #: 排序
    sort: Optional[int]
    #: 触发时机 [BEFORE_CREATE_SAVE-新建保存前、BEFORE_UPDATE_SAVE-更新保存前]
    triggerType: str
    uniqueKey: Optional[str]
    #: 赋值内容
    valueContent: Optional[str]
    #: 校验错误列表
    errorMsgList: List[RuleErrorMsg]
    #: 规则参数
    ruleParams: Optional[List[RuleParam]]


class SequenceInstance(BaseModel):
    #: 当前值
    currentValue: Optional[int]
    #: 序列编号
    sequenceId: Optional[str]
    #: 序列主键
    sequenceKey: Optional[str]
    #: 序列名称
    sequenceName: Optional[str]


class SimpleSpaceConnectionConfig(BaseModel):
    space: str
    dbType: Optional[str]
    dbName: Optional[str]
    schema_: Optional[str] = Field(alias='schema')
    edgedbName: str
    edgedbSchema: Optional[str]
    createTime: Optional[str]
    updateTime: Optional[str]


class QlGlobalVariableVO(BaseModel):
    #: 编码
    code: Optional[str]
    #: 类型
    type: Optional[str]
    #: 值
    value: Optional[str]


class QlRecordVO(BaseModel):
    #: 应用标识
    app: Optional[str]
    #: 空间标识
    space: Optional[str]
    #: 用户id
    userId: Optional[str]
    #: 创建时间
    createTime: Optional[str]
    #: 应用标识
    globalVariables: Optional[List[QlGlobalVariableVO]]
    #: 主键标识
    qlRecordId: Optional[str]
    #: QL类型：deepql|graphql|analysisql
    qlType: Optional[str]
    #: ql编码
    recordCode: Optional[str]
    #: 记录内容
    recordContent: Optional[str]
    #: 记录名称
    recordName: Optional[str]
    #: 记录类型：个人PERSONAL /公共：PUBLIC
    recordType: Optional[str]
    #: 变量
    variables: Any


ObjectParam.update_forward_refs()
ObjectLinkParam.update_forward_refs()
