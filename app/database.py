from sqlmodel import SQLModel, Field, Session, create_engine, select


DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True)

