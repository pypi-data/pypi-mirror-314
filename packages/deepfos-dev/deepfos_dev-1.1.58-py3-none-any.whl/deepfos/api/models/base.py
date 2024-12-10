import json
from collections import defaultdict

from pydantic import BaseModel as PydanticBaseModel, Field, validator
from pydantic.fields import FieldInfo
# noinspection PyProtectedMember
from pydantic.main import ModelMetaclass
from pydantic.generics import GenericModel
from typing import Any, TypeVar, Generic, no_type_check, Dict

__all__ = [
    "HeaderModel",
    "Response",
    "BaseModel",
    "BaseModelPlus",
    "Group",
    "AutoField",
    "GenericResponse",
    "GResponse",
]


class Group(FieldInfo):
    def __init__(self, default, group_id, at_least=1, at_most=1, **kwargs):
        """
        Args:
            default: 默认值，同FieldInfo
            group_id: 组ID，id相同并且属于同一个类的被视为同一组
            at_least: 同组中至少需提供多少参数
            at_most: 同组中至多可以提供多少参数
            **kwargs: 同FieldInfo
        """
        self.at_most = at_most
        self.at_least = at_least
        self.group_id = group_id
        super().__init__(default, **kwargs)


class AutoField(FieldInfo):
    pass


def _enable_groupfield(group: Dict[str, Group]):
    grp = list(group.values())[-1]
    _field = list(group.keys())[-1]
    at_least, at_most = grp.at_least, grp.at_most
    restriction_msg = f"字段{list(group.keys())}至少需提供{at_least}个，" \
                      f"至多{at_most}个。"
    for g in group.values():
        g.description = f"{g.description}({restriction_msg})"

    # noinspection PyUnusedLocal
    def _validator(cls, v, values, field):
        assigned_fields = set(k for k, v in values.items() if v is not None)
        if v is not None:
            assigned_fields.add(field.name)

        grp_assigned_fields = group.keys() & assigned_fields
        if not at_least <= len(grp_assigned_fields) <= at_most:
            if grp_assigned_fields:
                field_info = f"实际赋值的字段为：{grp_assigned_fields}"
            else:
                field_info = "实际任何字段都未赋值。"
            raise AssertionError(f"{restriction_msg}{field_info}")

    return f"_validator_{grp.group_id}", \
           validator(_field, always=True, allow_reuse=True)(_validator)


class MetaModel(ModelMetaclass):
    @no_type_check  # noqa C901
    def __new__(mcs, name, bases, namespace, **kwargs):  # noqa C901
        groups = defaultdict(dict)
        ann = namespace.get('__annotations__', {})
        namespace['__autofields__'] = auto_fields = {}

        for k, v in namespace.items():
            if isinstance(v, Group):
                groups[v.group_id][k] = v
            if isinstance(v, AutoField):
                auto_fields[k] = ann[k]
                ann[k] = Any

        for grp in groups.values():
            k, v = _enable_groupfield(grp)
            namespace[k] = v

        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        return cls


class BaseModel(PydanticBaseModel):
    @classmethod
    def construct_from(cls, *models: 'BaseModel', **extra):
        """
        基于PydanticBaseModel.contruct，删除不在_fields_set中的属性
        """
        fields_set = set(cls.__fields__.keys())
        attrs = {}
        for m in models:
            attrs.update({
                k: getattr(m, k)
                for k in (m.__fields_set__ & fields_set)
            })
        attrs.update({
            k: extra[k] for
            k in (fields_set & extra.keys())
        })

        return cls.construct(fields_set, **attrs)

    @classmethod
    def quick_parse(cls, **fields):
        # todo recursive parse dict to model
        valid_fields = {}

        for field_name, value in fields.items():
            if field_name not in cls.__fields__:
                continue


class BaseModelPlus(BaseModel, metaclass=MetaModel):
    """
    可支持使用Group定义字段, AutoField定义字段

    Examples:
        GroupA = functools.partial(Group, group_id='aaa', at_most=2)
        GroupB = functools.partial(Group, group_id='bbb')

        class TestModel(GroupBaseModel):
            a: str = GroupA(None, description='hello a')
            b: str = GroupA(None, description='hello b')
            c: int = GroupA(None, description='hello c')
            d: int = GroupB(None, description='hello d')
            e: int = GroupB(None, description='hello e')

        按照上述定义的TestModel，在实例化时，a,b,c字段至少需提供1个，至多2个.
        d, e字段至少提供1个，至多1个。
        并且会在openapi中添加相应描述
    """

    def __getattribute__(self, item):
        attr = super().__getattribute__(item)

        if item.startswith('__'):
            return attr
        if item not in self.__autofields__:
            return attr
        if not isinstance(attr, str):
            return attr

        model = self.__autofields__[item]
        new_attr = model.construct_from(**json.loads(attr))
        setattr(self, item, new_attr)
        return new_attr

    def dict(
        self, *, include=None, exclude=None, by_alias=False, skip_defaults=None,
        exclude_unset=False, exclude_defaults=False, exclude_none=False,
    ):
        ori_dict = super().dict(
            include=include,
            exclude=exclude,
            skip_defaults=skip_defaults,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        for field in self.__autofields__:
            if not isinstance(ori := ori_dict[field], str):
                ori_dict[field] = json.dumps(ori)
        return ori_dict


class HeaderModel(BaseModel):
    app: str
    space: str
    user: str
    language: str


class Response(BaseModel):
    status: bool = Field(description='接口状态信息')
    code: int = Field(None, description='接口错误码')
    message: str = Field(None, description='接口错误信息')
    data: Any = Field(None, description='接口返回值')


DataT = TypeVar('DataT')


class GenericResponse(GenericModel, Generic[DataT]):
    status: bool = Field(description='接口状态信息')
    code: int = Field(None, description='接口错误码')
    message: str = Field(None, description='接口错误信息')
    data: DataT = Field(None, description='接口返回值')


class GResponse:
    """
    特殊的泛型响应模型类
    用于更好地提供响应中data字段的文档信息

    Examples:
         ``GResponse[str, description]`` 可以返回一个 GenericResponse[str] 类型，
         并且description的内容可以展示在接口文档中。
    """
    memo = {}
    data_desc = Response.__fields__['data'].field_info.description

    def __class_getitem__(cls, item):
        model_key = (cls, item)
        if model_key in cls.memo:
            return cls.memo[model_key]

        if isinstance(item, tuple):
            *params, description = item
            ann = item[0]
        else:
            params = (item, )
            ann = item
            description = cls.data_desc

        model_name = f"Resp{GenericModel.__concrete_name__(params)}{description}"

        data_field = Field(None, description=description)

        model = type(model_name, (Response,), {
            '__annotations__': {'data': ann},
            'data': data_field
        })
        cls.memo[model_key] = model
        return model
