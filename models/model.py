from pydantic import BaseModel

class user(BaseModel):
    username: str
    password: str
    
class url(BaseModel):
    username: str
    org_url: str
    nickname: str