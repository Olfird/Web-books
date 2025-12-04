from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from app.core.config import database_url


engine = create_async_engine(
    url=database_url,
    pool_pre_ping=True, 
    pool_size=10, 
    max_overflow=20, 
    pool_recycle=1800,  
)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)