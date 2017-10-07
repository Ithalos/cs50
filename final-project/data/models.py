from data.database import Base, create_table_metadata
from sqlalchemy import Column, String, Integer

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def __repr__(self):
        return "<User: (username = {}, password = {})>".format(self.username, self.password)


create_table_metadata()

