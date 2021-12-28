from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List,Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oath2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/")
#@router.get("/")
def get_posts(db: Session=Depends(get_db),
                    current_user: int = Depends(oath2.get_current_user),
                    limit:int=10,skip:int=0,search:Optional[str]=""):

#    posts = db.query(models.Post).filter(models.Post.title.contains
#            (search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).\
        filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate,
                       current_user: int = Depends(oath2.get_current_user),
                       db: Session=Depends(get_db)
                       ):
    # what is current user?

    new_post = models.Post( owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post  # return to user

#@router.get("/{id}",response_model=schemas.PostOut )
@router.get("/{id}")
async def get_post(id: int, current_user: int = Depends(oath2.get_current_user),
                   db: Session=Depends(get_db)): #The response object
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).\
        join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by\
        (models.Post.id).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post

# Delete entry
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session=Depends(get_db),
                      current_user: int=Depends(oath2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="no item with specified id")

    if post.owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update entry
@router.put("/{id}", response_model=schemas.Post)
async def update_post(id: int,updated_post: schemas.PostCreate, db: Session=Depends(get_db),
                      current_user: int = Depends(oath2.get_current_user) ):
    # This is sufficate to grab the item from DB
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first() # This line was the problem
