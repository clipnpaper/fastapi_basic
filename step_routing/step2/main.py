from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from typing import List, Dict

app = FastAPI()
# templates = Jinja2Templates(directory="templates")

# 기본 endpoint
@app.get('/')
async def read_root():
    return {"message" : "Hello, FastAPI!"}

# 경로 파라메터 /items/1    /items/2    /users/123
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id" : item_id}

# users/123/items/foobar
@app.get("/users/{user_id}/items/{item_name}")
async def read_item(user_id, item_name):
    return {"user_id" : user_id, "item_name" : item_name}

# 쿼리 파라메터 /items/?skip=2&limit=20 
@app.get("/items/")
def read_items(skip = 0, limit = 10):
    return {"skip" : skip, "limit" : limit}

# Dict 데이터 타입을 요청 바디로 받는 라우트 예제
@app.post("/items/")
def create_item(item: dict):
    return {"item": item}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    return {"item_id": item_id, "updated_item": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item {item_id} has been deleted"}