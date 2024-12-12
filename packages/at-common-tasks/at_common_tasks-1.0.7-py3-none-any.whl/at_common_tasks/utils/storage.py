from typing import List, Type, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from at_common_models.base import Base
import logging
from dataclasses import dataclass

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
        """
        Initialize the StorageService with database settings
        
        Args:
            settings: DatabaseSettings object containing connection details
        """
        if not self._is_initialized:
            self.engine = create_engine(
                f"mysql+mysqlconnector://",
                connect_args={
                    'host': settings.host,
                    'port': settings.port,
                    'user': settings.user,
                    'password': settings.password,
                    'database': settings.database,
                    'charset': 'utf8mb4',
                    'collation': 'utf8mb4_general_ci'
                }
            )
            self.SessionLocal = sessionmaker(bind=self.engine)
            self._is_initialized = True

    def query(self, model_class: Type[Base], filters: Optional[List] = None) -> List[Base]:
        """
        Query objects from storage with optional filters
        
        Args:
            model_class: SQLAlchemy model class to query
            filters: Optional list of SQLAlchemy filter conditions
            
        Returns:
            List of model instances matching the query
        """
        if not self._is_initialized:
            raise RuntimeError("StorageService must be initialized with database settings first")

        with self.SessionLocal() as session:
            try:
                query = session.query(model_class)
                if filters:
                    query = query.filter(*filters)
                return query.all()
            except SQLAlchemyError as e:
                session.rollback()
                logging.error(f"Query error occurred: {str(e)}")
                raise

# Global instance
_storage_service = StorageService()

def init_storage(host: str, port: int, user: str, password: str, database: str) -> StorageService:
    """
    Initialize the global storage service instance
    
    Args:
        host: Database host
        port: Database port
        user: Database user
        password: Database password
        database: Database name
        
    Returns:
        Initialized StorageService instance
    """
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