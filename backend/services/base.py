# app/services/base.py
from typing import TypeVar, Generic
from ..dao.base import BaseDAO

T = TypeVar('T')


class BaseService(Generic[T]):
    """服务层基类"""

    def __init__(self, dao: BaseDAO[T]):
        self.dao = dao
