import abc
from importlib._modulespec import ModuleSpec
import sys
import types
from typing import Mapping, Optional, Sequence, Union

_Path = Union[bytes, str]

class Loader(metaclass=abc.ABCMeta):
    def load_module(self, fullname: str) -> types.ModuleType: ...
    if sys.version_info >= (3, 3):
        def module_repr(self, module: types.ModuleType) -> str: ...
    if sys.version_info >= (3, 4):
        def create_module(self, spec: ModuleSpec) -> Optional[types.ModuleType]:
            ...
        # Not defined on the actual class for backwards-compatibility reasons,
        # but expected in new code.
        def exec_module(self, module: types.ModuleType) -> None: ...

class Finder(metaclass=abc.ABCMeta): ...
    # Technically this class defines the following method, but its subclasses
    # in this module violate its signature. Since this class is deprecated, it's
    # easier to simply ignore that this method exists.
    #@abc.abstractmethod
    #def find_module(self, fullname: str,
    #                path: Sequence[_Path] = None) -> Optional[Loader]: ...

class ResourceLoader(Loader):
    @abc.abstractmethod
    def get_data(self, path: _Path) -> bytes: ...

class InspectLoader(Loader):
    def is_package(self, fullname: str) -> bool: ...
    def get_code(self, fullname: str) -> Optional[types.CodeType]: ...
    def load_module(self, fullname: str) -> types.ModuleType: ...
    @abc.abstractmethod
    def get_source(self, fullname: str) -> Optional[str]: ...
    if sys.version_info >= (3, 4):
        def exec_module(self, module: types.ModuleType) -> None: ...
    if sys.version_info == (3, 4):
        def source_to_code(self, data: Union[bytes, str],
                           path: str = '<string>') -> types.CodeType: ...
    elif sys.version_info >= (3, 5):
        @staticmethod
        def source_to_code(self, data: Union[bytes, str],
                           path: str = '<string>') -> types.CodeType: ...

class ExecutionLoader(InspectLoader):
    @abc.abstractmethod
    def get_filename(self, fullname: str) -> _Path: ...
    def get_code(self, fullname: str) -> Optional[types.CodeType]: ...

class SourceLoader(ResourceLoader, ExecutionLoader):
    def path_mtime(self, path: _Path) -> Union[int, float]: ...
    def set_data(self, path: _Path, data: bytes) -> None: ...
    def get_source(self, fullname: str) -> Optional[str]: ...
    if sys.version_info >= (3, 3):
        def path_stats(self, path: _Path) -> Mapping[str, Any]: ...


if sys.version_info >= (3, 3):
    class MetaPathFinder(Finder):
        def find_module(self, fullname: str,
                        path: Optional[Sequence[_Path]]) -> Optional[Loader]:
            ...
        def invalidate_caches(self) -> None: ...
        if sys.version_info >= (3, 4):
            # Not defined on the actual class, but expected to exist.
            def find_spec(self, fullname: str, path: Optional[Sequence[_Path]],
                          target: types.ModuleType = None
                         ) -> Optional[ModuleSpec]:
                ...

    class PathEntryFinder(Finder):
        def find_module(self, fullname: str) -> Optional[Loader]: ...
        def find_loader(self, fullname: str
                       ) -> Tuple[Optional[Loader], Sequence[_Path]]: ...
        def invalidate_caches(self) -> None: ...
        if sys.version_info >= (3, 4):
            # Not defined on the actual class, but expected to exist.
            def find_spec(self, fullname: str,
                          target: types.ModuleType = None
                         ) -> Optional[ModuleSpec]:
                ...

    class FileLoader(ResourceLoader, ExecutionLoader):
        name = ... # type: str
        path = ... # type: _Path
        def __init__(self, fullname: str, path: _Path) -> None: ...
        def get_data(self, path: _Path) -> bytes: ...
        def get_filename(self, fullname: str) -> _Path: ...
