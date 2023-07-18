import os
import json
import datetime
from sqlite_utils import Database
from app import helper

# 输入文字生成网页字体
def font_text_woff2(content: str, fontid: str):
    temp_rand = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    path_list = []

    db = Database('fonts.db')
    font = list(db['fonts'].rows_where('id = ?', [fontid], limit=1))
    
    if len(font) > 0:
        font = font[0]
    else:
        return []

    font_family = font['family']
    file_path = font['file_path']
    file_list = json.loads(font['file_list'])

    save_path = "temp/" + temp_rand
    file_css = save_path + "/" + fontid + ".css"

    path_list.append(file_css)

    for file in file_list:
        try:
            file_name = file['file_name']
            file_name2 = os.path.splitext(file_name)[0]
            # 生成web字体
            saved_path = helper.font_to_woff2(content, file_path + "/" + file_name, save_path + '/' + file_name2 + ".woff2")

            path_list.append(saved_path)
        except Exception as e:
            pass
        continue
    # 生成字体样式
    helper.font_to_css(file_css, font_family, file_list)

    return path_list