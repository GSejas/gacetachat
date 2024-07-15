# models.py
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, DateTime, JSON, ForeignKey, Boolean, Float
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum
import uuid

# pm2 start /home/fastapiuser/gacetachat/venv/bin/python -- '/home/fastapiuser/gacetachat/download_gaceta.py' --name download_gaceta

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    language = Column(String, default="en")
    hashed_password = Column(String)

class ContentTemplate(Base):
    __tablename__ = "content_templates"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)

    # Relationship with PromptTemplate
    prompts = relationship("Prompt", back_populates="content_template")

class Prompt(Base):
    __tablename__ = "prompts"
    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey('content_templates.id'))
    prompt_text = Column(Text)
    template = relationship("ContentTemplate", back_populates="prompts")
    name = Column(String(255))
    short_description = Column(Text)

    content_template = relationship("ContentTemplate", back_populates="prompts")
    
    
class ExecutionState(enum.Enum):
    INIT = "INIT"
    EXECUTED = "EXECUTED"
    FAILED = "FAILED"
    OUTDATED = "OUTDATED"


class ExecutionSession(Base):
    __tablename__ = "execution_sessions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    content_template_id = Column(Integer, ForeignKey('content_templates.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String, default=ExecutionState.INIT.value)

    content_template = relationship("ContentTemplate")
    user = relationship("User")
    logs = relationship("ContentExecutionLog", back_populates="execution_session")

class ContentExecutionLog(Base):
    __tablename__ = "execution_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('users.id'))
    template_id = Column(Integer, ForeignKey('content_templates.id'))
    prompt_id = Column(Integer, ForeignKey('prompts.id'))
    query_response_id = Column(String, ForeignKey('query_answers.id'))
    execution_session_id = Column(String, ForeignKey('execution_sessions.id'))
    state = Column(String, default=ExecutionState.INIT.value)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    # response_text = Column(Text, nullable=True)  # To store the response of the executed prompt


    user = relationship("User")
    template = relationship("ContentTemplate")
    prompt = relationship("Prompt")
    output = relationship("PromptQueryResponse")
    execution_session = relationship("ExecutionSession")

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "template_id": self.template_id,
            "prompt_id": self.prompt_id,
            "query_response_id": self.query_response_id,
            "execution_session_id": self.execution_session_id,
            "state": self.state,
            "error_message": self.error_message,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class PromptQueryResponse(Base):
    __tablename__ = 'query_answers'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    raw_prompt = Column(Text)
    response = Column(Text, nullable=True)
    sources = Column(Text, nullable=True)
    prompt_template_id = Column(Text, ForeignKey('prompts.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    execution_logs = relationship("ContentExecutionLog", back_populates="output")



class GacetaPDF(Base):
    __tablename__ = 'gacetas'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String, nullable=False)

from db import engine

Base.metadata.create_all(engine)