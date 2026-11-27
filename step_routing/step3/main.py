# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Memo(BaseModel):
    title: str
    content: str
    is_important: Optional[bool] = None


# class Item(BaseModel):
#     name: str                          # 필수
#     description: Optional[str] = None  # 선택, 기본값 None
#     price: float                       # 필수
#     tax: float = 0.1                   # 선택, 기본값 0.1

@app.post("/memos/")
async def create_item(memo: Memo):
    return {"memo": memo.model_dump()}

# 실행: uvicorn main:app --reload