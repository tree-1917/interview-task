from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

# Association table to represent users as members of organizations
organization_membership = Table(
    'organization_membership',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('organization_id', Integer, ForeignKey('organizations.id'), primary_key=True),
    Column('member_at', DateTime, default=datetime.datetime.now, nullable=True)
)

# User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    
    # Relationship for organizations owned by the user
    organizations_owned = relationship("Organization", back_populates="owner")

    # Relationship for organizations the user is a member of
    organizations_member = relationship(
        "Organization",
        secondary=organization_membership,
        back_populates="members"
    )

# TokenTable model
class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer, ForeignKey('users.id'))
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450), nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)

# Organization model
class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    created_date = Column(DateTime, default=datetime.datetime.now)
    
    # Relationship to the owner (a single user)
    owner = relationship("User", back_populates="organizations_owned")

    # Relationship for members of the organization (many users)
    members = relationship(
        "User",
        secondary=organization_membership,
        back_populates="organizations_member"
    )
