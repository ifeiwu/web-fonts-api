from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import FileResponse
from starlette.background import BackgroundTask
from fastapi.middleware.cors import CORSMiddleware
import os
from app import helper
from app.font_css_title import font_css_title
from app.font_css_all import font_css_all
from app.font_text_woff2 import font_text_woff2
from app.font_css_words import font_css_words

app = FastAPI()

# CORS（跨源资源共享）
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
# end

class Item(BaseModel):
    dirname: str
    content: str


@app.get("/")
def root():
    return {"Hello": "Web Fonts api"}


# 生成指定文字web字体
@app.post("/build/")
def build(item: Item):
    return font_text_woff2(item.content, item.dirname)


# 生成web字体和样式
@app.get("/build-css/")
def build_css():
    font_css_words()
    font_css_title()
    font_css_all()


# 获取所有字体列表，对象属性形式
@app.get("/font-list/")
def fonts():
    return helper.font_list()

# 获取所有字体列表，键值对形式
@app.get("/font-list-kv/")
def fonts():
    return helper.font_list_kv()


# 响应下载web字体
@app.get("/download/")
def download(filename: str):

    helper.remove_empty_dir("temp/")

    return FileResponse(filename, background=BackgroundTask(lambda: os.remove(filename)))