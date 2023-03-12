from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import FileResponse
from starlette.background import BackgroundTask
from fastapi.middleware.cors import CORSMiddleware
import os
from app import helper
from app.font_css_title import font_css_title
from app.font_css_all import font_css_all
from app.font_css_text import font_css_text

app = FastAPI()

# CORS（跨源资源共享）
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# end

class Item(BaseModel):
    dirname: str
    content: str


@app.get("/")
def root():
    return {"Hello": "Web Fonts api"}

# 生成指定文字的网页字体
@app.post("/build/")
def build(item: Item):
    return font_css_text(item.content, item.dirname)


# 生成字体标题样式
@app.get("/build-css-title/")
def build_css_title():
    font_css_title()


@app.get("/build-css-all/")
def build_css_all():
    font_css_all()

# 获取所有字体列表
@app.get("/font-list/")
def fonts():
    return helper.font_list()

@app.get("/font-list-kv/")
def fonts():
    return helper.font_list_kv()


# 响应下载字体
@app.get("/download/")
def download(filename: str):

    helper.remove_empty_dir("temp/")

    return FileResponse(filename, background=BackgroundTask(lambda: os.remove(filename)))