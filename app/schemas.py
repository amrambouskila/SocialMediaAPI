from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime

# Users Table
class User(BaseModel):
    email: EmailStr
    password: str

class Create_User(User):
    pass

class Update_User(User):
    pass

class User_Response(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class User_Login(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Token_Data(BaseModel):
    id: str


# Posts Table
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class Create_Post(Post):
    pass

class Update_Post(Post):
    pass

class Post_Response(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner: User_Response

    class Config:
        orm_mode = True

class Post_Votes_Response(BaseModel):
    Post_Table: Post_Response
    votes: int

    class Config:
        orm_mode = True

# Votes Table
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
