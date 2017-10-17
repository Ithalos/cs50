from data.database import Base, create_table_metadata
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    memos = relationship("Memo", back_populates="user", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<User: (username = {}, password = {})>".format(self.username, self.password)


class Memo(Base):

    __tablename__ = "memos"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="memos")

    def __repr__(self):
        return "<Memo: (text = {})>".format(self.text)


create_table_metadata()

