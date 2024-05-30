#!/usr/bin/env python3
"""module docs for user.py"""
from typing import Any
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """User model declaration"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)  # the integer primary key
    email = Column(String(250))  # a non-nullable string
    hashed_password = Column(String(250))  # a non-nullable string
    session_id = Column(String(250))  # a nullable string
    reset_token = Column(String(250))  # a nullable string
