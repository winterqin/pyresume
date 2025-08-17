# app/dao/base.py
from typing import TypeVar, Generic, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

T = TypeVar('T')  # 泛型类型参数


class BaseDAO(Generic[T]):
    """所有DAO的基类，提供CRUD基础操作"""

    def __init__(self, model: type[T], db: Session):
        self.model = model
        self.db = db

    def get(self, id: int) -> Optional[T]:
        return self.db.get(self.model, id)

    def get_all(
            self,
            skip: int = 0,
            limit: int = 100,
            order_by: str = None,
            desc_order: bool = False
    ) -> List[T]:
        query = self.db.query(self.model)
        if order_by:
            column = getattr(self.model, order_by, None)
            if column is not None:
                query = query.order_by(desc(column) if desc_order else asc(column))
        return query.offset(skip).limit(limit).all()

    def create(self, obj: T) -> T:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: T) -> T:
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: int) -> bool:
        obj = self.get(id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True



