
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    persona = Column(String, index=True)
    message = Column(Text)
    response = Column(Text)
    timestamp = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Conversation(id={self.id}, persona='{self.persona}', message='{self.message[:30]}...', response='{self.response[:30]}...')>"
