from fastapi import FastAPI
from pydantic import BaseModel
from fontbro import Font
from starlette.responses import FileResponse
import random
import time
import os
import helper

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


# 生成字体标题样式
@app.get("/build-title/")
def build_title():

    filename2 = ""
    css_file_name = ""
    timestamp = str(int(time.time()))

    dirs = os.listdir("fonts/")

    for dirname in dirs:
        csscode = ""
        css_file_name = "css/" + dirname + "/title/" + dirname + ".css"

        if os.path.exists(css_file_name):
            continue

        files = os.listdir("fonts/" + dirname)

        for filename in files:
            ext = os.path.splitext(filename)[1]

            if ext == '.ttf' or ext == '.otf':
                font_title = helper.font_title(dirname)
                font = Font("fonts/" + dirname + "/" + filename)
                font.subset(text=font_title)
                filename2 = filename.replace(".ttf", "").replace(".otf", "")
                font.save_as_woff2(filepath="css/" + dirname + "/title/" + filename2 + ".woff2", overwrite=True)

                weight = filename2.split('-')
                if len(weight) > 1:
                    weight = weight[1].lower()
                else:
                    weight = "regular"

                weight = helper.font_weight(weight)

                csscode += "@font-face{font-family:'" + dirname + "';src:url('" + filename2 + ".woff2') format('woff2');font-weight:" + weight + ";font-style:normal;font-display:swap;}"

        cssfile = open(css_file_name, 'w')
        cssfile.write(csscode)
        cssfile.close()


# 获取所有字体列表
@app.get("/fonts/")
def fonts():

    return helper.font_list()


# 响应下载字体
@app.get("/download/")
def download(file: str):

    return FileResponse(file)