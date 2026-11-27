# main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Memo(BaseModel):
    title: str
    content: str
    is_important: Optional[bool] = None

class UserSignup(BaseModel):
    username: str
    email: str
    password: str
    age: int
    marketing_agree: Optional[bool] = False

class Order(BaseModel):
    product_name: str
    price: float
    quantity: int
    coupon_code: Optional[str] = None

class MemoUpdate(BaseModel):
    title: str
    content: str
    is_important: Optional[bool] = None

class Todo(BaseModel):
    task: str
    priority: Optional[int] = 3
    done: Optional[bool] = False

todo_db = []

@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse(request, 'home.html')

@app.post("/memos/")
async def create_item(memo: Memo):
    return {"memo": memo.model_dump()}

@app.post("/users/signup")
async def signup(user_signup: UserSignup):
    return {"message": f"{user_signup.username}님, 가입을 환영합니다!", 
            "user": {"username": user_signup.username, 
                     "email": user_signup.email,
                     "age": user_signup.age,
                     "marketing_agree": user_signup.marketing_agree}
}

@app.post("/orders/")
async def orders(orders: Order):
    total_price = orders.price * orders.quantity
    discount = total_price / 10 if orders.coupon_code == "WELCOME10" else 0
    final_price = total_price - discount
    return {"product_name": orders.product_name, 
            "quantity": orders.quantity, 
            "total_price": total_price, 
            "discount": discount, 
            "final_price": final_price}
# 실행: uvicorn main:app --reload

@app.put("/memos/{memo_id}")
async def update_memo(memo_id : int, memo_update: MemoUpdate):
    return {"memo_id": memo_id, 
            "updated_memo": memo_update.model_dump()}

@app.post("/todos/")
async def todos_db(todos: Todo):
    todo_db.append(todos)
    return {"todo_id": len(todo_db) , "todo" : todos.model_dump() }

@app.get("/todos/")
async def get_todo(skip : int = 0, limit : int = 10):
    return {"total": len(todo_db), "todos": todo_db[skip : skip + limit]}

@app.get("/todos/page")
async def todos_page(request: Request):
    return templates.TemplateResponse(request, 'home2.html', {"todos": todo_db})

@app.get("/todos/{todo_id}")
async def detail_todo(todo_id: int):
    if not (0 <= todo_id < len(todo_db)):
        return {"error": f"{todo_id}번 할 일이 없습니다."}
    return {"todo_id": todo_id, "todo" : todo_db[todo_id].model_dump()}

@app.put("/todos/{todo_id}")
async def update_todo(todo_id : int, todo_update: Todo):
    if not (0 <= todo_id < len(todo_db)):
        return {"error": f"{todo_id}번 할 일이 없습니다."}
    todo_db[todo_id] = todo_update
    return {"todo_id": todo_id, 
            "updated_todo": todo_update.model_dump()}

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    if not (0 <= todo_id < len(todo_db)):
        return {"error": f"{todo_id}번 할 일이 없습니다."}
    deleted_todo = todo_db.pop(todo_id)
    return {"todo_id": todo_id,
            "deleted_todo": deleted_todo.model_dump() }