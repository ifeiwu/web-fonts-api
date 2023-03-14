import os
from app import helper

def font_css_title():

    dirs = os.listdir("fonts/")

    for dirname in dirs:
        filenames = []
        fontfamily = dirname

        save_path = "css/title/" + dirname + "/"

        filecss = save_path + dirname + ".css"

        if os.path.exists(filecss):
            continue

        files = os.listdir("fonts/" + dirname)

        for filename in files:
            ext = os.path.splitext(filename)[1]

            if ext == '.ttf' or ext == '.otf':
                # 字体标题
                font_title = helper.font_title(dirname)
                # 没有扩展名
                filename2 = os.path.splitext(filename)[0]
                # 生成web字体
                helper.font_to_woff2(font_title, "fonts/" + dirname + "/" + filename, save_path + filename2 + ".woff2")

                filenames.append(filename2)
        # 生成字体样式
        helper.font_to_css(fontfamily, filenames, filecss)