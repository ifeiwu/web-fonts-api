import os
from app import helper

def font_css_words():

    dirs = os.listdir("fonts/")

    words = {"3500":"zh-cn", "5000":"zh-cn", "7000":"zh-cn", "5000":"zh-tw"}

    for number, lang in words.items():
        for dirname in dirs:
            filenames = []
            fontfamily = dirname

            save_path = "css/" + number + "/" + lang + "/" + dirname + "/"

            filecss = save_path + dirname + ".css"

            if os.path.exists(filecss):
                continue

            files = os.listdir("fonts/" + dirname)

            for filename in files:
                name_ext = os.path.splitext(filename)
                # 提取扩展名
                ext = name_ext[1]

                if ext == '.ttf' or ext == '.otf':
                    # 读取文件内容
                    content = helper.read_file("words/" + lang + "_" + number + ".txt")
                    # 去除扩展名
                    filename2 = name_ext[0]
                    # 生成web字体
                    helper.font_to_woff2(content, "fonts/" + dirname + "/" + filename, save_path + filename2 + ".woff2")

                    filenames.append(filename2)
            # 生成字体样式
            helper.font_to_css(fontfamily, filenames, filecss)