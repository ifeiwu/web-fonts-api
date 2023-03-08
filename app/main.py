from fastapi import FastAPI
from pydantic import BaseModel
from fontbro import Font
from starlette.responses import FileResponse
import random
import time
import os

app = FastAPI()


class Item(BaseModel):
    dirname: str
    content: str


@app.get("/")
def root():
    return {"Hello": "Web Fonts api"}

# 生成指定文字的网页字体
@app.post("/build/")
def build(item: Item):
    temp_rand = str(round(time.time() * 1000)) + str(random.randint(0, 1000))
    file_list = []

    font_list = os.listdir("fonts/" + item.dirname)

    for filename in font_list:
        ext = os.path.splitext(filename)[1]
        if ext == '.ttf' or ext == '.otf':
            font = Font("fonts/" + item.dirname + "/" + filename)
            font.subset(text=item.content)
            filename2 = filename.replace(".ttf", "").replace(".otf", "")
            saved_path = font.save_as_woff2(filepath="temp/" + temp_rand + '/' + filename2 + ".woff2", overwrite=True)
            file_list.append(saved_path)

    return file_list


# 获取所有字体列表
@app.get("/fonts/")
def fonts():
    items = {}
    dirs = os.listdir("fonts/")

    for dirname in dirs:
        files = os.listdir("fonts/" + dirname)
        for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext == '.txt':
                items[dirname] = os.path.splitext(filename)[0]

    return items


# 响应下载字体
@app.get("/download/")
def download(file: str):

    return FileResponse(file)