from typing import TypeVar, Generic, Callable, List, Generator

T = TypeVar('T')
R = TypeVar('R')

I = TypeVar('I')
O = TypeVar('O')


class Stream(Generic[I, O]):
    def __init__(self,
                 data: List[I],
                 gen: Callable[[List[I]], Generator[O, None, None]] = lambda xs: (x for x in xs)
                 ):
        self.data = data
        self.gen = gen

    def map(self,
            converter: Callable[[I], O],
            filter: Callable[[I], bool] = lambda x: True
            ) -> 'Stream[T, U]':
        new_gen: Callable[[List[I]], Generator[O, None, None]] = lambda ls: (converter(item) for item in self.gen(ls)
                                                                             if filter is not None and filter(item))
        return Stream(self.data, gen=new_gen)

    def filter(self, filter: Callable[[I], bool]):
        new_gen: Callable[[List[I]], Generator[O, None, None]] = lambda ls: (item for item in self.gen(ls) if
                                                                             filter is not None and filter(item))
        return Stream(self.data, gen=new_gen)

    def get(self) -> Generator[O, None, None]:
        return self.gen(self.data)

    def list(self) -> List[O]:
        return list(self.gen(self.data))


if __name__ == '__main__':
    data = Stream([1, 2, 3, 4]) \
        .map(lambda x: x * x) \
        .filter(lambda x: x > 3) \
        .list()
    print(data)

    # def get(self, list_of_data: List[I]) -> List[O]:
    #     return ()
    #
    # def gen(self, list_of_data: List[I]) -> Generator[O, None, None]:
    #     return (item for item in self.gen(list_of_data))


class Scope(Generic[T]):
    def __init__(self, obj: T):
        self._obj = obj

    def ensureExists(self) -> 'Scope[T]':
        if self._obj is None:
            raise Exception("object is None")
        else:
            return self

    def apply(self, f: Callable[[T], T]) -> 'Scope[T]':
        return Scope(f(self._obj))

    def applyIf(self, predicate: Callable[[T], bool], f: Callable[[T], T]) -> 'Scope[T]':
        if self._obj is None:
            return self
        if predicate(self._obj):
            f(self._obj)
            return Scope(self._obj)
        else:
            return self

    def map(self, f: Callable[[T], R]) -> 'Scope[R]':
        return Scope(f(self._obj))

    def verify(self, predicate: Callable[[T], bool],
               msg: Callable[[T], str] = lambda x: f"verification failure: {x}") -> 'Scope[T]':
        result = predicate(self._obj)
        if result:
            return self
        else:
            raise Exception(msg(self._obj))

    def get(self) -> 'T':
        return self._obj
