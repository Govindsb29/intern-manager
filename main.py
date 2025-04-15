import datetime
from models import Base
from database import engine
from fastapi import FastAPI, HTTPException, Depends
import models
from datetime import datetime
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy import text

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    print("runn")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/interns")
def add_intern(name:str, db: Session=Depends(get_db)):
    intern = models.Intern(name=name)
    db.add(intern)
    db.commit()
    return{"intern_id":intern.intern_id}


@app.post("/Attendance/login")
def Log_in(intern_id:int, db:Session=Depends(get_db)):
    intern_check = db.query(models.Intern).filter(models.Intern.intern_id==intern_id).first()
    if intern_check is None:
        raise Exception("Intern ID doesn't exist")

    attendance = models.Attendance(
        intern_id = intern_check.intern_id,
        name = intern_check.name,
        date = datetime.now().date(),
        login_time = datetime.now()
    )

    db.add(attendance)
    db.commit()


@app.post("/Attendance/logout")
def Log_out(intern_id:int, db:Session=Depends(get_db)):
    logout_time = datetime.now()

    logged_in = db.query(models.Attendance).filter(models.Attendance.intern_id==intern_id, models.Attendance.date == datetime.now().date()).first()
    if logged_in is None:
        raise Exception("Intern ID doesn't exist")
    
    query1 = text("""update attendance set logout_time = :logout_time, duration = timediff(:logout_time, login_time) where intern_id = :intern_id and date = CURDATE()""")
    db.execute(query1,{"intern_id":intern_id, "logout_time":logout_time})
    db.commit()


@app.post("/Tasks/Assign")
def assign(admin_id:int,intern_id:int, task:str, db:Session=Depends(get_db)):
    admin_check = db.query(models.Admin).filter(models.Admin.admin_id==admin_id).first()
    if admin_check is None:
        raise Exception("Admin ID invalid")
    intern_check = db.query(models.Intern).filter(models.Intern.intern_id==intern_id).first()
    if intern_check is None:
        raise Exception("Intern ID doesn't exist")
    
    assign = models.Tasks(
        intern_id = intern_check.intern_id,
        name = intern_check.name,
        task = task
    )

    db.add(assign)
    db.commit()


@app.post("/Tasks/Complete")
def complete(intern_id:int,status:str,db:Session=Depends(get_db)):
    intern_check = db.query(models.Intern).filter(models.Intern.intern_id==intern_id).first()
    if intern_check is None:
        raise Exception("Intern ID doesn't exist")
    
    query2 = text("""update tasks set task_status =:status where intern_id=:intern_id""")
    db.execute(query2,{"intern_id":intern_check.intern_id, "status":status})
    db.commit()
