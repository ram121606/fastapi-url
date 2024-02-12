from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import os

url = os.environ.get('DB_URL')

engine = create_engine(url)
Base = declarative_base()

def connection():
    try:    
        if(engine):
            print(":)")
    except Exception as e:
        print(e)
