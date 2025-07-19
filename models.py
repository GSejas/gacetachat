# models.py
import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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
    template_id = Column(Integer, ForeignKey("content_templates.id"))
    prompt_text = Column(Text)
    name = Column(String(255))
    short_description = Column(Text)
    alias = Column(String(255), unique=True, nullable=True)  # Add alias field
    scheduled_execution = Column(Boolean, default=True)  # New field
    doc_aware = Column(Boolean, default=True)  # New field

    content_template = relationship("ContentTemplate", back_populates="prompts")

    def to_json(self):
        return {
            "id": self.id,
            "template_id": self.template_id,
            "prompt_text": self.prompt_text,
            "name": self.name,
            "short_description": self.short_description,
            "alias": self.alias,
            "scheduled_execution": self.scheduled_execution,  # Include in JSON representation
        }


class ExecutionState(enum.Enum):
    INIT = "INIT"
    EXECUTED = "EXECUTED"
    APPROVED = "APPROVED"
    FAILED = "FAILED"
    OUTDATED = "OUTDATED"


class ExecutionSession(Base):
    __tablename__ = "execution_sessions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    content_template_id = Column(
        Integer, ForeignKey("content_templates.id"), nullable=True
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String, default=ExecutionState.INIT.value)
    document_id = Column(String, ForeignKey("gacetas.id"), nullable=True)

    content_template = relationship("ContentTemplate")
    user = relationship("User")
    logs = relationship("ContentExecutionLog", back_populates="execution_session")
    messages = relationship("ChatMessage", back_populates="chat_session")
    gaceta = relationship("GacetaPDF", back_populates="exec_sess")
    is_approved = Column(Boolean, default=False)

    def to_json(self):
        return {
            "id": self.id,
            "content_template_id": self.content_template_id,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "status": self.status,
            "document_id": self.document_id,
            "is_approved": self.is_approved,
        }


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("execution_sessions.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)

    chat_session = relationship("ExecutionSession", back_populates="messages")


class ContentExecutionLog(Base):
    __tablename__ = "execution_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"))
    template_id = Column(Integer, ForeignKey("content_templates.id"))
    prompt_id = Column(Integer, ForeignKey("prompts.id"))
    query_response_id = Column(String, ForeignKey("query_answers.id"))
    execution_session_id = Column(String, ForeignKey("execution_sessions.id"))
    state = Column(String, default=ExecutionState.INIT.value)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    # response_text = Column(Text, nullable=True)  # To store the response of the executed prompt

    user = relationship("User")
    template = relationship("ContentTemplate")
    prompt = relationship("Prompt")
    output = relationship("PromptQueryResponse", back_populates="execution_logs")
    execution_session = relationship("ExecutionSession", back_populates="logs")

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
            "updated_at": self.updated_at,
        }


class PromptQueryResponse(Base):
    __tablename__ = "query_answers"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    raw_prompt = Column(Text)
    response = Column(Text, nullable=True)
    sources = Column(Text, nullable=True)
    prompt_template_id = Column(Text, ForeignKey("prompts.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    execution_logs = relationship("ContentExecutionLog", back_populates="output")

    def to_json(self):
        return {
            "id": self.id,
            "raw_prompt": self.raw_prompt,
            "response": self.response,
            "sources": self.sources,
            "prompt_template_id": self.prompt_template_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class GacetaPDF(Base):
    __tablename__ = "gacetas"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String, nullable=False)

    exec_sess = relationship("ExecutionSession", back_populates="gaceta")

    def to_json(self):
        return {
            "id": self.id,
            "date": self.date,
            "file_path": self.file_path,
        }


from sqlalchemy import Column, Date, Integer


class GlobalQueryCount(Base):
    __tablename__ = "global_query_counts"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True)
    count = Column(Integer, default=0)


from db import engine

Base.metadata.create_all(engine)
