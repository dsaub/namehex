from sqlmodel import Session, create_engine
from . import settings

engine = create_engine(settings.DB_STRING)
