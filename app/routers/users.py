<<<<<<< HEAD
from .. import schemas
from fastapi import status, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix='/users', tags=['Users'])

@router.get('/', response_model=List[schemas.User_Response])
def get_users(db: Session=Depends(get_db)):
    users = db.query(models.User_Table).all()
    return users

@router.get('/latest', response_model=schemas.User_Response)
def get_latest_user(db: Session=Depends(get_db)):
    latest_user = db.query(models.User_Table).order_by(models.User_Table.id.desc()).first()
    return latest_user

@router.get('/{id}', response_model=schemas.User_Response)
def get_user(id: int, db: Session=Depends(get_db)):
    user = db.query(models.User_Table).get(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User id {id} was not found')
    return user

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User_Response)
def create_user(user: schemas.Create_User, db: Session=Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User_Table(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session=Depends(get_db)):
    deleted_user = db.query(models.User_Table).get(id)
    db.query(models.User_Table).filter_by(id=id).delete(synchronize_session=False)
    db.commit()
    if deleted_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post id {id} was not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.User_Response)
def update_user(id: int, updated_post: schemas.Update_User, db: Session=Depends(get_db)):
    user_query = db.query(models.User_Table).filter(models.User_Table.id == id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post id {id} was not found')
    user_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
=======
from .. import models, schemas, utils
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix='/users', tags=['Users'])

@router.get('/', response_model=List[schemas.User_Response])
def get_users(db: Session=Depends(get_db)):
    users = db.query(models.User_Table).all()
    return users

@router.get('/latest', response_model=schemas.User_Response)
def get_latest_user(db: Session=Depends(get_db)):
    latest_user = db.query(models.User_Table).order_by(models.User_Table.id.desc()).first()
    return latest_user

@router.get('/{id}', response_model=schemas.User_Response)
def get_user(id: int, db: Session=Depends(get_db)):
    user = db.query(models.User_Table).get(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User id {id} was not found')
    return user

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User_Response)
def create_user(user: schemas.Create_User, db: Session=Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User_Table(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session=Depends(get_db)):
    deleted_user = db.query(models.User_Table).get(id)
    db.query(models.User_Table).filter_by(id=id).delete(synchronize_session=False)
    db.commit()
    if deleted_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post id {id} was not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.User_Response)
def update_user(id: int, updated_post: schemas.Update_User, db: Session=Depends(get_db)):
    user_query = db.query(models.User_Table).filter(models.User_Table.id == id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post id {id} was not found')
    user_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
>>>>>>> 28fbc88f2d44fd64d2eeaa3f5bef0db91ad3df05
    return user_query.first()