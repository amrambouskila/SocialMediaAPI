<<<<<<< HEAD
import sqlalchemy
from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional


# def get_data_from_my_sql(select_query):
#     try:
#         cnx = mysql.connector.connect(user=user, password=password,
#                                       host=host,
#                                       database=database)
#         cursor = cnx.cursor(buffered=True)
#         cursor.execute(select_query)
#         cursor.close()
#         cnx.close()
#         return cursor.fetchall()
#     except mysql.connector.Error as err:
#         print(err)
#         print("Error Code:", err.errno)
#         print("SQLSTATE", err.sqlstate)
#         print("Message", err.msg)
#     return None

# def post_data_to_my_sql(insert_query, new_post):
#     try:
#         cnx = mysql.connector.connect(user=user, password=password,
#                                       host=host,
#                                       database=database)
#         cursor = cnx.cursor(buffered=True)
#         cursor.execute(insert_query, (new_post.title, new_post.content, new_post.published))
#         cnx.commit()
#         cursor.execute('select * from practice_api.posts where title = %s and content = %s and published = %s', (new_post.title, new_post.content, new_post.published))
#         post = cursor.fetchone()
#         cursor.close()
#         cnx.close()
#         return post
#     except mysql.connector.Error as err:
#         print(err)
#         print("Error Code:", err.errno)
#         print("SQLSTATE", err.sqlstate)
#         print("Message", err.msg)
#     return None

# def delete_data_from_my_sql(delete_query, id):
#     try:
#         cnx = mysql.connector.connect(user=user, password=password,
#                                       host=host,
#                                       database=database)
#         cursor = cnx.cursor(buffered=True)
#         cursor.execute(f'select * from practice_api.posts where id = {id}')
#         deleted_post = cursor.fetchone()
#         cursor.execute(delete_query, (str(id),))
#         cnx.commit()
#         cursor.close()
#         cnx.close()
#         return deleted_post
#     except mysql.connector.Error as err:
#         print(err)
#         print("Error Code:", err.errno)
#         print("SQLSTATE", err.sqlstate)
#         print("Message", err.msg)
#     return None

# def update_data_from_my_sql(update_query, id, updated_post):
#     try:
#         cnx = mysql.connector.connect(user=user, password=password,
#                                       host=host,
#                                       database=database)
#         cursor = cnx.cursor(buffered=True)
#         cursor.execute(update_query, (updated_post.title, updated_post.content, updated_post.published, id))
#         cnx.commit()
#         cursor.execute(f'select * from wwig.posts where id = {id}')
#         updated_post = cursor.fetchone()
#         cursor.close()
#         cnx.close()
#         return updated_post
#     except mysql.connector.Error as err:
#         print(err)
#         print("Error Code:", err.errno)
#         print("SQLSTATE", err.sqlstate)
#         print("Message", err.msg)
#     return None

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.get('/', response_model=List[schemas.Post_Votes_Response])
def get_posts(db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    posts = db.query(models.Post_Table, func.count(models.Vote_Table.post_id).label('votes')).join(
        models.Vote_Table, models.Vote_Table.post_id == models.Post_Table.id, isouter=True).group_by(
        models.Post_Table.id).filter(models.Post_Table.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get('/latest', response_model=List[schemas.Post_Votes_Response])
def get_latest_post(db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    latest_post =  db.query(models.Post_Table, func.count(models.Vote_Table.post_id).label('votes')).join(
        models.Vote_Table, models.Vote_Table.post_id == models.Post_Table.id, isouter=True).group_by(
        models.Post_Table.id).order_by(sqlalchemy.desc(models.Post_Table.id)).all()[:1]
    print(latest_post)

    return latest_post

@router.get('/{id}', response_model=List[schemas.Post_Votes_Response])
def get_post(id: int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post =  db.query(models.Post_Table, func.count(models.Vote_Table.post_id).label('votes')).join(
        models.Vote_Table, models.Vote_Table.post_id == models.Post_Table.id, isouter=True).group_by(
        models.Post_Table.id).filter(models.Post_Table.id == id).all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post id {id} was not found')
    return post

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post_Response)
def create_posts(post: schemas.Create_Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post_Table(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post_Table).get(id)
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized to perform requested action')
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post id {id} was not found')
    db.query(models.Post_Table).filter_by(id=id).delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.Post_Response)
def update_post(id: int, updated_post: schemas.Update_Post, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post_Table).filter(models.Post_Table.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post id {id} was not found')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized to perform requested action')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
=======
import sqlalchemy
from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional


# def get_data_from_my_sql(select_query):
#     try:
#         cnx = mysql.connector.connect(user=user, password=password,
#                                       host=host,
#                                       database=database)
#         cursor = cnx.cursor(buffered=True)
#         cursor.execute(select_query)
#         cursor.close()
#         cnx.close()
#         return cursor.fetchall()
#     except mysql.connector.Error as err:
#         print(err)
#         print("Error Code:", err.errno)
#         print("SQLSTATE", err.sqlstate)
#         print("Message", err.msg)
#     return None

# def post_data_to_my_sql(insert_query, new_post):
#     try:
#         cnx = mysql.connector.connect(user=user, password=password,
#                                       host=host,
#                                       database=database)
#         cursor = cnx.cursor(buffered=True)
#         cursor.execute(insert_query, (new_post.title, new_post.content, new_post.published))
#         cnx.commit()
#         cursor.execute('select * from practice_api.posts where title = %s and content = %s and published = %s', (new_post.title, new_post.content, new_post.published))
#         post = cursor.fetchone()
#         cursor.close()
#         cnx.close()
#         return post
#     except mysql.connector.Error as err:
#         print(err)
#         print("Error Code:", err.errno)
#         print("SQLSTATE", err.sqlstate)
#         print("Message", err.msg)
#     return None

# def delete_data_from_my_sql(delete_query, id):
#     try:
#         cnx = mysql.connector.connect(user=user, password=password,
#                                       host=host,
#                                       database=database)
#         cursor = cnx.cursor(buffered=True)
#         cursor.execute(f'select * from practice_api.posts where id = {id}')
#         deleted_post = cursor.fetchone()
#         cursor.execute(delete_query, (str(id),))
#         cnx.commit()
#         cursor.close()
#         cnx.close()
#         return deleted_post
#     except mysql.connector.Error as err:
#         print(err)
#         print("Error Code:", err.errno)
#         print("SQLSTATE", err.sqlstate)
#         print("Message", err.msg)
#     return None

# def update_data_from_my_sql(update_query, id, updated_post):
#     try:
#         cnx = mysql.connector.connect(user=user, password=password,
#                                       host=host,
#                                       database=database)
#         cursor = cnx.cursor(buffered=True)
#         cursor.execute(update_query, (updated_post.title, updated_post.content, updated_post.published, id))
#         cnx.commit()
#         cursor.execute(f'select * from wwig.posts where id = {id}')
#         updated_post = cursor.fetchone()
#         cursor.close()
#         cnx.close()
#         return updated_post
#     except mysql.connector.Error as err:
#         print(err)
#         print("Error Code:", err.errno)
#         print("SQLSTATE", err.sqlstate)
#         print("Message", err.msg)
#     return None

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.get('/', response_model=List[schemas.Post_Votes_Response])
def get_posts(db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    posts = db.query(models.Post_Table, func.count(models.Vote_Table.post_id).label('votes')).join(
        models.Vote_Table, models.Vote_Table.post_id == models.Post_Table.id, isouter=True).group_by(
        models.Post_Table.id).filter(models.Post_Table.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get('/latest', response_model=List[schemas.Post_Votes_Response])
def get_latest_post(db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    latest_post =  db.query(models.Post_Table, func.count(models.Vote_Table.post_id).label('votes')).join(
        models.Vote_Table, models.Vote_Table.post_id == models.Post_Table.id, isouter=True).group_by(
        models.Post_Table.id).order_by(sqlalchemy.desc(models.Post_Table.id)).all()[:1]
    print(latest_post)

    return latest_post

@router.get('/{id}', response_model=List[schemas.Post_Votes_Response])
def get_post(id: int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post =  db.query(models.Post_Table, func.count(models.Vote_Table.post_id).label('votes')).join(
        models.Vote_Table, models.Vote_Table.post_id == models.Post_Table.id, isouter=True).group_by(
        models.Post_Table.id).filter(models.Post_Table.id == id).all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post id {id} was not found')
    return post

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post_Response)
def create_posts(post: schemas.Create_Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post_Table(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post_Table).get(id)
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized to perform requested action')
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post id {id} was not found')
    db.query(models.Post_Table).filter_by(id=id).delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.Post_Response)
def update_post(id: int, updated_post: schemas.Update_Post, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post_Table).filter(models.Post_Table.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post id {id} was not found')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized to perform requested action')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
>>>>>>> 28fbc88f2d44fd64d2eeaa3f5bef0db91ad3df05
    return post_query.first()