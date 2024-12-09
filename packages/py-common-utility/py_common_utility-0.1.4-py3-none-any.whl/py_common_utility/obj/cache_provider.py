from typing import Callable, TypeVar, Generic, Dict

T = TypeVar("T")


class CacheProvider(Generic[T]):

    def __init__(self, name: str, cache_map: Dict[str, T], provide: Callable[[], T]):
        self.name: str = name
        self.cache_map: Dict[str, T] = cache_map
        self.provide: Callable[[], T] = provide

    def get_instance(self) -> T:
        if self.name not in self.cache_map:
            self.cache_map[self.name] = self.provide()
        return self.cache_map[self.name]


# ti = CacheProvider[str]("cache", [], lambda: "1233")
