from sqlalchemy import Boolean, Column, Integer, String, DateTime,Date,ForeignKey,PrimaryKeyConstraint
from database import Base
from sqlalchemy import Time
import datetime


class Intern(Base):
    __tablename__ = "interns"
    intern_id = Column(Integer,primary_key = True)
    name = Column(String(100))

class Admin(Base):
    __tablename__ = "admin_table"

    admin_id = Column(Integer, primary_key=True)
    admin_name = Column(String(100))


    

class Attendance(Base):
    __tablename__ = "attendance"
    intern_id = Column(Integer, ForeignKey("interns.intern_id"),primary_key=True)
    name = Column(String(100))
    date = Column(Date, default=datetime.date.today)
    login_time = Column(DateTime)
    logout_time = Column(DateTime)
    duration = Column(Time)

class Tasks(Base):
    __tablename__ = "tasks"
    intern_id = Column(Integer, ForeignKey("interns.intern_id"))
    task_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    task = Column(String(255))
    task_status = Column(String(15), default="Not Completed")



