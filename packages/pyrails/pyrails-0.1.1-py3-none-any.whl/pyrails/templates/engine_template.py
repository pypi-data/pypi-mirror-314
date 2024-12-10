engine_template="""from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config.settings import settings

engine = create_engine(url=settings.DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False, class_=Session)"""