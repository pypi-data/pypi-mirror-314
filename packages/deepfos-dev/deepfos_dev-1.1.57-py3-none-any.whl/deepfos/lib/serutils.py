from __future__ import annotations

import datetime
import decimal
import functools
import uuid
from dataclasses import dataclass
from typing import Any

import edgedb
from edgedb.introspect import introspect_object as intro
from edgedb.datatypes import datatypes


@dataclass(frozen=True)
class Context:
    frame_desc: Any = None


@functools.singledispatch
def serialize(o, ctx: Context = Context()):
    raise TypeError(f'无法序列化类型: {type(o)}')


@functools.singledispatch
def deserialize(o):
    raise TypeError(f'无法反序列化类型: {type(o)}')


@deserialize.register
def to_object(o: dict):
    _id = o.pop('id', None)
    ordered_attr = o.keys()
    obj_cls = datatypes.create_object_factory(
        id='property' if _id else 'implicit',
        **{k: 'link' if isinstance(o[k], dict) else 'property' for k in ordered_attr}
    )
    actual_id = None
    if _id:
        if isinstance(_id, str):
            actual_id = uuid.UUID(_id)
        elif isinstance(_id, uuid.UUID):
            actual_id = _id
    return obj_cls(
        actual_id,
        *[deserialize(o[k]) for k in ordered_attr]
    )


@deserialize.register
def to_set(o: list):
    return [deserialize(ele) for ele in o]


@deserialize.register
def to_tuple(o: tuple):
    return tuple(deserialize(ele) for ele in o)


@deserialize.register(int)
@deserialize.register(float)
@deserialize.register(str)
@deserialize.register(bytes)
@deserialize.register(bool)
@deserialize.register(type(None))
@deserialize.register(datetime.datetime)
def to_scalar(o):
    return o


@serialize.register
def _tuple(o: edgedb.Tuple, ctx: Context = Context()):
    if ctx.frame_desc is None:
        return tuple(serialize(el) for el in o)
    return tuple(
        serialize(el, Context(frame_desc=ctx.frame_desc[idx])) 
        for idx, el in enumerate(o)
    )


@serialize.register
def _namedtuple(o: edgedb.NamedTuple, ctx: Context = Context()):
    if ctx.frame_desc is None:
        return {attr: serialize(getattr(o, attr)) for attr in dir(o)}
    return {
        attr: serialize(getattr(o, attr), Context(frame_desc=ctx.frame_desc[attr]))
        for attr in ctx.frame_desc
    }


@serialize.register
def _linkset(o: edgedb.LinkSet, ctx: Context = Context()):
    return [serialize(el, ctx) for el in o]


@serialize.register
def _link(o: edgedb.Link, ctx: Context = Context()):
    ret = {}
    if ctx.frame_desc is None:
        for lprop in dir(o):
            if lprop in {'source', 'target'}:
                continue
            ret[f'@{lprop}'] = serialize(getattr(o, lprop))

        ret.update(_object(o.target))
        return ret

    lprops = list(map(lambda x: f'@{x}', (set(dir(o)) - {'source', 'target'})))
    for field in ctx.frame_desc:
        new_ctx = Context(frame_desc=ctx.frame_desc[field])
        if field in lprops:
            ret[field] = serialize(getattr(o, field[1:]), new_ctx)
        else:
            ret[field] = serialize(getattr(o.target, field), new_ctx)
    return ret


def ignore_implicited_fields(o: edgedb.Object):
    return set(dir(o)) - {desc.name for desc in intro(o).pointers if desc.implicit}


@serialize.register
def _object(o: edgedb.Object, ctx: Context = Context()):
    ret = {}

    if ctx.frame_desc is None:
        for attr in ignore_implicited_fields(o):
            try:
                ret[attr] = serialize(o[attr])
            except (KeyError, TypeError):
                ret[attr] = serialize(getattr(o, attr))
        return ret

    for attr in (desc := ctx.frame_desc):
        try:
            ret[attr] = serialize(o[attr], Context(frame_desc=desc[attr]))
        except (KeyError, TypeError):
            ret[attr] = serialize(getattr(o, attr), Context(frame_desc=desc[attr]))

    return ret


@serialize.register(edgedb.Set)
@serialize.register(edgedb.Array)
def _set(o, ctx: Context = Context()):
    return [serialize(el, ctx) for el in o]


@serialize.register(int)
@serialize.register(float)
@serialize.register(str)
@serialize.register(bytes)
@serialize.register(bool)
@serialize.register(type(None))
@serialize.register(datetime.timedelta)
@serialize.register(datetime.date)
@serialize.register(datetime.datetime)
@serialize.register(datetime.time)
@serialize.register(edgedb.RelativeDuration)
@serialize.register(uuid.UUID)
@serialize.register(decimal.Decimal)
def _scalar(o, ctx: Context = Context()):
    return o


@serialize.register
def _enum(o: edgedb.EnumValue, ctx: Context = Context()):
    return str(o)
