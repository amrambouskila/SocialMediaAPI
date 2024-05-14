<<<<<<< HEAD
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users, auth, votes

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get('/')
def root():
    return {'message': 'Welcome to my API'}

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
=======
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users, auth, votes

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get('/')
def root():
    return {'message': 'Welcome to my API'}

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
>>>>>>> 28fbc88f2d44fd64d2eeaa3f5bef0db91ad3df05
