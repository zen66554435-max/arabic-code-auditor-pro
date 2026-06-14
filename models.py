"""
Arabic Code Auditor Pro - Database Models
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(200))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    projects = relationship("Project", back_populates="owner")
    scans = relationship("Scan", back_populates="user")

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'))
    repo_url = Column(String(500))
    language = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="projects")
    scans = relationship("Scan", back_populates="project")

class Scan(Base):
    __tablename__ = 'scans'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    scan_type = Column(String(50), nullable=False)  # code, project, security
    status = Column(String(50), default='pending')  # pending, running, completed, failed
    total_files = Column(Integer, default=0)
    total_issues = Column(Integer, default=0)
    security_findings = Column(Integer, default=0)
    code_quality_score = Column(Float, default=0.0)
    results = Column(JSON)
    scan_duration = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    project = relationship("Project", back_populates="scans")
    user = relationship("User", back_populates="scans")
    reports = relationship("Report", back_populates="scan")

class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey('scans.id'))
    report_type = Column(String(50), nullable=False)  # html, pdf, json, excel
    file_path = Column(String(500))
    file_size = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    scan = relationship("Scan", back_populates="reports")

class Plugin(Base):
    __tablename__ = 'plugins'

    id = Column(Integer, primary_key=True)
    plugin_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    name_ar = Column(String(200))
    version = Column(String(50))
    author = Column(String(200))
    description = Column(Text)
    description_ar = Column(Text)
    plugin_type = Column(String(50))
    is_enabled = Column(Boolean, default=True)
    is_installed = Column(Boolean, default=False)
    config = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Setting(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    value_type = Column(String(50), default='string')
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(Integer)
    details = Column(JSON)
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db(database_url: str = "sqlite:///aca.db"):
    """Initialize database"""
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    """Get database session"""
    Session = sessionmaker(bind=engine)
    return Session()
