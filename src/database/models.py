from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    JSON,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship

from src.database.database import Base


class Operator(Base):
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    max_leads = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    
    source_weights = relationship("SourceOperator", back_populates="operator")
    contacts = relationship("Contact", back_populates="operator")


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())
    
    operator_weights = relationship("SourceOperator", back_populates="source")
    contacts = relationship("Contact", back_populates="source")


class SourceOperator(Base):
    __tablename__ = "source_operators"

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("sources.id", ondelete="CASCADE"))
    operator_id = Column(Integer, ForeignKey("operators.id", ondelete="CASCADE"))
    weight = Column(Integer)
    enabled = Column(Boolean, default=True)
    
    source = relationship("Source", back_populates="operator_weights")
    operator = relationship("Operator", back_populates="source_weights")


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True)
    external_id = Column(String, nullable=False, unique=True)
    payload = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    contacts = relationship("Contact", back_populates="lead")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey("leads.id", ondelete="CASCADE"))
    source_id = Column(Integer, ForeignKey("sources.id", ondelete="CASCADE"))
    operator_id = Column(Integer, ForeignKey("operators.id", ondelete="SET NULL"), nullable=True)
    status = Column(String, default="active")
    payload = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    
    lead = relationship("Lead", back_populates="contacts")
    source = relationship("Source", back_populates="contacts")
    operator = relationship("Operator", back_populates="contacts")