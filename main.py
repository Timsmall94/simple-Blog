from random import randrange
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
app=FastAPI()


class Post(BaseModel):
    title:str
    content:str

my_post=[{"id":1,"title":"title of Post1", "content":"content of Post1"},
         {"id":2,"title":"title of Post2", "content":"content of Post2"},
         {"id":3,"title":"title of Post3", "content":"content of Post3"},
         {"id":4,"title":"title of Post4", "content":"content of Post4"}
         ]
def findpost(id):
    for p in my_post:
        if p["id"]==id:
            return p
        
def index_post(id):
    for i, p in enumerate(my_post):
        if p["id"]==id:
            return i 
    
@app.get('/post')
def getAllPost():
    # for i in my_post:
    #     return i   
    return {"data":my_post}

@app.post('/post')
def createPost(new_post:Post):
    post_dict=new_post.dict()
    post_dict['id']= randrange(1, 1000)
    my_post.append(post_dict)
    return {"New_Post":post_dict}

@app.get('/post/latest')
def getLatest():
    latest=my_post[len(my_post)-1]
    return {"latest_Post":latest}

@app.get('/post/{id}')
def GetpostById(id:int):
    foundpost= findpost(id)
    if not foundpost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'the post with id {id} not found')
    return {"details":foundpost}

@app.put('/post/{id}')
def updatePost(id:int, newly_updated:Post):
    foundpost=index_post(id)
    if foundpost== None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'the post with id {id} not found')
    post_dict =newly_updated.dict()
    post_dict["id"]=id
    my_post[foundpost]=post_dict
    return {"Updated Details":post_dict}

@app.delete('/post/{id}')
def DeletePost(id:int):
    foundpost=index_post(id)
    if not foundpost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'the post with id {id} not found')
    my_post.remove(foundpost)
    return {"deleted succefully"}

