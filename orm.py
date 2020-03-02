from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey, Date 
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    password = Column(String)
    salt = Column(String)

    __table_args__ = (
        UniqueConstraint('username'),
    )

    def __repr__(self):
        return 'User('\
            f'username={self.username}, ' \
            f'firstname={self.firstname}, ' \
            f'lastname={self.lastname}' \
            ')'


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(String, primary_key=True)
    userid = Column(Integer, ForeignKey('users.id'))

    user = relationship("User")


class Contests(Base):
    __tablename__ = 'contests'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    createdBy = Column(String, ForeignKey('users.username'))
    startDate = Column(Date)
    endDate = Column(Date)


class ContestMembership(Base):
    __tablename__ = 'contestMembership'

    contestid = Column(Integer, ForeignKey('contests.id'), primary_key=True)
    userid = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role = Column(String, primary_key=True)
