from __future__ import annotations

import os
from abc import abstractmethod, ABC
from typing import TypeVar, Optional

from holytools.logging import Loggable, LogLevel

DictType = TypeVar(name='DictType', bound=dict)

# ---------------------------------------------------------

class BaseConfigs(Loggable, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._map = {None : {}}
        self._populate_map()

    @abstractmethod
    def _populate_map(self):
        pass

    @staticmethod
    def _as_abspath(path: str) -> str:
        path = os.path.expanduser(path=path)
        path = os.path.abspath(path)
        return path

    # ---------------------------------------------------------
    # interface

    def get(self, key : str, section : Optional[str] = None) -> Optional[str]:
        if len(key.split()) > 1:
            raise ValueError(f'Key must not contain whitespaces, got : \"{key}\"')
        try:
            config_value = self._map[section][key]
        except KeyError:
            self.log(msg=f'Could not find key \"{key}\" under section \"{section}\" in configs', level=LogLevel.WARNING)
            config_value = None

        return config_value

    def set(self, key : str, value : str, section : Optional[str] = None):
        if not section in self._map:
            self._map[section] = {}
        section = self._map[section]
        if key in section:
            raise ValueError(f'Key \"{key}\" already exists in settings')
        section[key] = value
        self._update_resource()

    def get_sectionless_map(self) -> dict[str, str]:
        return self._map[None]

    @abstractmethod
    def _update_resource(self):
        pass



