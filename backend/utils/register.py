# framework/crud/registry.py
from typing import Dict, Type
from sqlalchemy.ext.declarative import DeclarativeMeta

class ModelRegistry:
    _registry: Dict[str, Type[DeclarativeMeta]] = {}
    
    @classmethod
    def register(cls, model: Type[DeclarativeMeta]):
        """注册模型类"""
        cls._registry[model.__name__] = model
        return model
        
    @classmethod
    def get_registered_models(cls):
        """获取所有已注册模型"""
        return cls._registry