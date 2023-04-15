from datetime import time
from random import randrange
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from . import models, schemas
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

#integrating for creating all the models
models.Base.metadata.create_all(engine)

app = FastAPI()
    

#routing
@app.get("/")
#decorator
def get_User():
    return {"Hello": "Sudip"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return {"data": posts}

@app.get("/posts")
def get_Post(db: Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return {'data': posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def creat_posts(post: schemas.Post, db: Session = Depends(get_db)):
    new_post = models.Posts(**post.dict())
    # This ORM Enter only one post at a time =>  new_post = models.Posts(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data" : new_post}
#The order in the column does effect

@app.get("/posts/latest")
def get_latest_post():
    post = ''
    return {"detail" : post}

@app.get("/posts/{id}")
def get_post(id: int, db : Session = Depends(get_db)):
    fetch_post = db.query(models.Posts).filter(models.Posts.id == id).first()
    print(fetch_post)
    if not fetch_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'Post with ID: {id} was not Found')
    return{"post_detail" : fetch_post}

@app.delete("/posts/{id}")
def delete_post(id: int, db : Session = Depends(get_db)):
    delete_post = db.query(models.Posts).filter(models.Posts.id == id)
    if delete_post.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Post with Id: {id} doesnot found.")
    delete_post.delete(synchronize_session = False)
    db.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    update_post = post_query.first()
    
    #if the id is not found : 
    if update_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Post with Id: {id} doesnot found.")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}
    