import os
import datetime
from app import helper

# 输入文字生成web字体
def font_text_woff2(words: str, dirname: str):

    temp_rand = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')

    file_list = []

    font_list = os.listdir("fonts/" + dirname)

    for filename in font_list:
    
        name_ext = os.path.splitext(filename)
        # 提取扩展名
        ext = name_ext[1]

        if ext == '.ttf' or ext == '.otf':
            # 去除扩展名
            filename2 = name_ext[0]
            # 生成web字体
            saved_path = helper.font_to_woff2(words, "fonts/" + dirname + "/" + filename, "temp/" + temp_rand + '/' + filename2 + ".woff2")

            file_list.append(saved_path)

    return file_list