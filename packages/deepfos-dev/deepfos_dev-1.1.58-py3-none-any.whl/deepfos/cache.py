import functools
import weakref
from typing import Protocol

from cachetools import TTLCache, LRUCache

__all__ = [
    'Manager',
    'CustomedCache',
    'AppSeperatedBase',
    'SpaceSeperatedBase',
    'AppSeperatedTTLCache',
    'SpaceSeperatedTTLCache',
    'AppSeperatedLRUCache',
    'SpaceSeperatedLRUCache'
]


class CacheProtocol(Protocol):  # pragma: no cover
    def clear(self) -> None:
        ...


class CacheManager:
    def __init__(self):
        self._caches = []

    def create_cache(self, cache_factory, *args, **kwargs) -> CacheProtocol:
        cache = cache_factory(*args, **kwargs)
        self._caches.append(weakref.ref(cache, self._caches.remove))
        return cache

    def clear(self):
        for cache in self._caches:
            cache().clear()

    @property
    def currsize(self):
        return len(self._caches)

    def __repr__(self):  # pragma: no cover
        return repr([c() for c in self._caches])


Manager = CacheManager()


class CustomedCache:
    def __init_subclass__(cls, *args, **kwargs):
        if hasattr(cls, 'clear'):
            cls.clear = cls.customed_clear(getattr(cls, 'clear'))
        if hasattr(cls, 'pop'):
            cls.pop = cls.customed_pop(getattr(cls, 'pop'))

        for funcname in {'__getitem__', '__setitem__', '__delitem__', '__contains__'}:
            if hasattr(cls, funcname):
                setattr(cls, funcname, cls.customize(getattr(cls, funcname)))

    @staticmethod
    def customize(ori_func):
        @functools.wraps(ori_func)
        def new_func(self, key, *args, **kwargs):
            key = (self.additional_key(), key)
            return ori_func(self, key, *args, **kwargs)

        return new_func

    @staticmethod
    def customed_clear(ori_func):
        @functools.wraps(ori_func)
        def new_func(self):
            for k in list(self):
                try:
                    del self[k[1]]
                except KeyError:
                    pass

        return new_func

    @staticmethod
    def customed_pop(ori_func):
        @functools.wraps(ori_func)
        def new_func(self, key, *args, **kwargs):
            key = key[1]
            return ori_func(self, key, *args, **kwargs)

        return new_func

    @classmethod
    def additional_key(cls):  # pragma: no cover
        raise NotImplementedError


class AppSeperatedBase(CustomedCache):
    @classmethod
    def additional_key(cls):
        from deepfos import OPTION
        return OPTION.api.header.get('app', 'Unknown_app')


class SpaceSeperatedBase(CustomedCache):
    @classmethod
    def additional_key(cls):
        from deepfos import OPTION
        return OPTION.api.header.get('space', 'Unknown_space')


class AppSeperatedTTLCache(TTLCache, AppSeperatedBase):
    pass


class SpaceSeperatedTTLCache(TTLCache, SpaceSeperatedBase):
    pass


class AppSeperatedLRUCache(LRUCache, AppSeperatedBase):
    pass


class SpaceSeperatedLRUCache(LRUCache, SpaceSeperatedBase):
    pass
