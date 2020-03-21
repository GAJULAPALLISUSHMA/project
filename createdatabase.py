from  sqlalchemy import ForeignKey, Column,Integer,String,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,backref
from sqlalchemy import create_engine
from flask_login import UserMixin



Base=declarative_base()

class Customers(Base,UserMixin):
	__tablename__='customer'
	id = Column(Integer,primary_key=True)
	Name=Column(String(500),nullable=True)
	Mobileno=Column(String(250),nullable=False)
	AdharNo=Column(String(250),nullable=False)
	Emailaddress=Column(String(250),unique=True)
	Password=Column(String(250),nullable=False)
	userType=Column(Integer)

class Central(Base):
	__tablename__='central'
	id=Column(Integer,primary_key=True)
	central_scheme_name=Column(String(2000),unique=True)
	image=Column(String(30500),nullable=False)
class CentralSchemes(Base):
	__tablename__='central_schemes'

	id=Column(Integer,primary_key=True)
	name=Column(String(500))
	description=Column(String(2000),nullable=False)
	link=Column(String(250),nullable=False)
	image=Column(String(30500),nullable=False)
	central_id=Column(Integer,ForeignKey('central.id'))
	centralDetail=relationship(Central)
class State(Base):
	__tablename__='state'
	id=Column(Integer,primary_key=True)
	statename=Column(String(2000),unique=True)
	image=Column(String(30500),nullable=False)
class StateSchemes(Base):
	__tablename__='state_schemes'

	id= Column(Integer,primary_key=True)
	name=Column(String(500))
	description=Column(String(2000),nullable=False)
	link=Column(String(250),nullable=False)
	image=Column(String(30500),nullable=False)
	state_id=Column(Integer,ForeignKey('state.id'))
	stateDetail=relationship(State)

class Details(Base):
	__tablename__='details'
	id = Column(Integer,primary_key=True)
	Name=Column(String(500),nullable=False)
	AdharNo=Column(String(250),nullable=False)
	Emailaddress=Column(String(250),unique=True)
	Mobileno=Column(String(250),nullable=False)
	AccountNO=Column(String(250),nullable=False)
	Age=Column(Integer,nullable=False)	
	image=Column(String(100),nullable=False)
	Category=Column(String(500),nullable=False)
	img=Column(String(100),nullable=False)
	userType=Column(Integer)

class Info(Base):
	__tablename__='info'
	id = Column(Integer,primary_key=True)
	Name=Column(String(500),nullable=False)
	AdharNo=Column(String(250),nullable=False)
	Mobileno=Column(String(250),nullable=False)
	AccountNO=Column(String(250),nullable=False)
	Age=Column(Integer,nullable=False)	
	image=Column(String(100),nullable=False)
	Category=Column(String(500),nullable=False)
	userType=Column(Integer)


class Suggestions(Base):
	__tablename__='Suggestions'
	id = Column(Integer,primary_key=True)
	Name=Column(String(100))
	
	Emailaddress=Column(String(100))
	Mobileno=Column(String(100))
	suggestions=Column(String(100))


class Reset_Token(Base):
	__tablename__='reset_tokens'
	id=Column(Integer,primary_key=True)
	tourister_id=Column(Integer,ForeignKey('customer.id'))
	token=Column(String(32),nullable=False)
	
		

engine=create_engine('sqlite:///SCHEMES.db')
Base.metadata.create_all(engine)	     