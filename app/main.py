from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.font_css_title import font_css_title
from app.font_css_all import font_css_all
from app.font_text_woff2 import font_text_woff2
from app.font_css_words import font_css_words
from app.fonts_db import fonts_db
from app import helper

app = FastAPI()
# 静态文件访问
app.mount("/css", StaticFiles(directory="css"), "css")

# CORS（跨源资源共享）
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
# end

# 构建自定义网页字体，POST请求数据对象类型
class BuildData(BaseModel):
    fontid: str
    content: str


@app.get("/")
def root():
    return {"Hello": "Web Fonts API"}


# 构建已知网页字体
@app.get("/build-css/")
def build_css():
    fonts_db()
    font_css_title()
    font_css_words()
    font_css_all()


# 构建自定义网页字体
@app.post("/build/")
def build(data: BuildData):
    return font_text_woff2(data.content, data.fontid)


# 获取一个字体对象
@app.get("/font/")
def font(id = None, family = None):
    return helper.font_one(id, family)


# 获取字体列表，数组形式
@app.get("/fonts/")
def fonts(lang = None, keyword = None, orderby = None, offset = None, limit = None):
    return helper.font_list('array', lang, keyword, orderby, offset, limit)


# 获取字体列表，对象形式
@app.get("/fonts-kv/")
def fonts_kv(lang = None, keyword = None, orderby = None, offset = None, limit = None):
    return helper.font_list('object', lang, keyword, orderby, offset, limit)


# 获取已经生成[css/文字数量/字体id]目录下所有文件
@app.get("/css-files/")
def css_files(fontid: str, number: str, lang = None):
    if lang == None:
        path = 'css/' + number + '/' + fontid
    else:
        path = 'css/' + number + '/' + lang + '/' + fontid

    return helper.read_css_files(path)


# 下载网页字体
@app.get("/download/")
def download(filename: str, action = None):
    return helper.download(filename, action)


# 更新英文字体源文件
@app.get("/download-google-fonts/")
def download_google_fonts():
    helper.download_google_fonts()