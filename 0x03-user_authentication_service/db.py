#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        # self._engine = create_engine("sqlite:///a.db", echo=True)
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """stores a new user to db"""
        new_user = User()  # create user instance
        # update it's attributes
        new_user.email = email
        new_user.hashed_password = hashed_password
        self._session.add(new_user)
        self.__session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """find users by a given key, value.
        Key must be a column name in db
        """
        table_columns = list(User.__dict__.keys())
        # print(table_columns)
        keyz = kwargs.keys()
        search = {}
        for key in keyz:
            if key not in table_columns:
                raise InvalidRequestError
            value = kwargs[key]
            search[key] = value
        found = self._session.query(User).filter_by(**search).first()
        # print(found.email)
        if not found:
            raise NoResultFound
        return found

    def update_user(self, user_id: int, **kwargs) -> None:
        """update a user whose, id is given"""
        table_columns = list(User.__dict__.keys())
        keyz = kwargs.keys()
        user = self.find_user_by(id=user_id)
        for key in keyz:
            if key not in table_columns:
                raise ValueError
            setattr(user, key, kwargs[key])
            # user.update(key, kwargs[key])
        # print(user.hashed_password)
        self._session.commit()
