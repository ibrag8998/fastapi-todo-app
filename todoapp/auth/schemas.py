from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    
    class Config:
        orm_mode = True


class UserInDB(User):
    password: str
    
    class Config:
        orm_mode = True
