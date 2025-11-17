from db.database import Base
from sqlalchemy import Integer,Column,String,Boolean, Float


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completion_status = Column(Boolean, default=False)