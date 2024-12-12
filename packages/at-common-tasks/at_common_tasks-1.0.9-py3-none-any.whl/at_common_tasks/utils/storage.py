from typing import List, Type, Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from at_common_models.base import Base
import logging
from urllib.parse import quote_plus
from dataclasses import dataclass
from sqlalchemy import select

@dataclass
class StorageSettings:
    host: str
    port: int
    user: str
    password: str
    database: str

class StorageService:
    _instance = None
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def init(self, settings: StorageSettings):
        """Initialize the StorageService with async database connection"""
        if not self._is_initialized:
            self.engine = create_async_engine(
                f"mysql+aiomysql://{quote_plus(settings.user)}:{quote_plus(settings.password)}@{settings.host}:{settings.port}/{settings.database}",
                connect_args={
                    'charset': 'utf8mb4'
                }
            )
            self.AsyncSessionLocal = async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            self._is_initialized = True

    async def query(
        self, 
        model_class: Type[Base], 
        filters: Optional[List] = None,
        sort: Optional[List] = None,
        limit: Optional[int] = None
    ) -> List[Base]:
        """Async query method"""
        if not self._is_initialized:
            raise RuntimeError("StorageService must be initialized with database settings first")

        async with self.AsyncSessionLocal() as session:
            try:
                query = select(model_class)
                if filters:
                    query = query.filter(*filters)
                if sort:
                    query = query.order_by(*sort)
                if limit:
                    query = query.limit(limit)
                
                result = await session.execute(query)
                return result.scalars().all()
            except SQLAlchemyError as e:
                await session.rollback()
                logging.error(f"Query error occurred: {str(e)}")
                raise

# Global instance
_storage_service = StorageService()

def init_storage(host: str, port: int, user: str, password: str, database: str) -> StorageService:
    """Async initialization of storage service"""
    settings = StorageSettings(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    _storage_service.init(settings)
    return _storage_service

def get_storage() -> StorageService:
    """
    Get the global storage service instance
    
    Returns:
        StorageService instance
    
    Raises:
        RuntimeError: If storage service is not initialized
    """
    if not _storage_service._is_initialized:
        raise RuntimeError("Storage service not initialized. Call init_storage first.")
    return _storage_service