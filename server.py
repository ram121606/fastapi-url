from fastapi import FastAPI
import uvicorn
from db.connection import connection, engine
from db.table import userTable, urlTable
from models.model import user,url
from sqlalchemy.orm import Session
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from typing import Tuple


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

connection()
userTable.metadata.create_all(engine)
userTable.metadata.create_all(engine)

@app.get('/')
def home():
    return '🙌'


@app.post('/register')
def register(payload: user):
    user = userTable(**payload.model_dump())
    print(user.username)
    session = Session(engine)
    data = session.query(userTable).filter(payload.username == userTable.username).first()
    if(data == None):
        session.add(user)
        session.commit()
        print("User added Successfully :)")
        result = False
    else:
        print("Already exists :(") 
        result = True
    session.close()
    return {'result': result}


@app.post('/login')
def login(payload: user):
    session = Session(engine)
    print(payload)
    data = session.query(userTable).filter(payload.username == userTable.username).first()
    if(data.password != payload.password):
        print("User not found :(")
        result = False
    else:
        print("Logged in :)")
        result = True
    session.close()
    return {'result': result}


@app.post('/url')
def url(payload: url):
    session = Session(engine)
    print(payload)
    data = urlTable(**payload.model_dump())
    print(data)
    exists = False
    update = False
    result = ''
    res = session.query(urlTable.username, urlTable.nickname).filter(data.username == urlTable.username, data.nickname == urlTable.nickname).first()
    con1 = data.username == urlTable.username
    con2 = data.org_url == urlTable.org_url
    #check if result is already present with given username and nickname
    if(res is not None):
        #if exists retrieve the related short_url by checking if org_url of both matches
        short = session.query(urlTable.short_url).filter(con1, con2).first()
        if(short is None):#if not matches short_url already linked
            print("Nickname linked :(")
            exists = True
            # return "exists"
        else:#else return short_url
            print(short[0])
            result = short[0]
    else:
        #if doesnot exists check if the given org_url is already present in the table
        original = session.query(urlTable.org_url).filter(data.username == urlTable.username, data.org_url == urlTable.org_url).first()
        print(original)
        if(original is not None):
            #if exists ask whether to overide with new nickname
            print("update??")
            update = True
        else:
            #else insert the record and return res
            data.short_url = os.environ.get('HOST') + data.username + '/' + data.nickname
            session.add(data)
            session.commit()
            print("data added")
            print(data.short_url)
            result = data.short_url
    session.close()
    return {'host': result, 'exists': exists, 'update': update}


@app.get('/{username}/{nickname}')
def redirect(username, nickname):
    session = Session(engine)
    result = session.query(urlTable.org_url).filter(username == urlTable.username, nickname == urlTable.nickname).first()[0]
    print(result)
    session.close()
    # print(result[0])
    return RedirectResponse(url = result)

@app.get('/{username}')
def details(username: str):
    # print(username)
    print("<>")
    session = Session(engine)
    result = session.query(urlTable.short_url, urlTable.org_url).filter(username == urlTable.username).all()
    final_result = [(i.short_url, i.org_url) for i in result]
    # print(final_result)
    return {'result': final_result}


if __name__ == "__main__":
    uvicorn.run('server:app', reload=True)