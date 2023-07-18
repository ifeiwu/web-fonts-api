import os
import json
from sqlite_utils import Database
from app import helper

def font_css_title():
    db = Database('fonts.db')
    fonts = db['fonts'].rows

    for font in fonts:
        font_id = font['id']
        file_path = font['file_path']
        font_family = font['family']
        font_title = font['title']
        file_list = json.loads(font['file_list'])

        css_name = font_family.replace(' ', '')

        save_path = 'css/title/' + font_id

        file_css = save_path + '/' + font_id + '.css'

        if os.path.exists(file_css):
            continue

        for file in file_list:
            try:
                file_name = file['file_name']
                file_name2 = os.path.splitext(file_name)[0]
                # 生成web字体
                helper.font_to_woff2(font_title, file_path + '/' + file_name, save_path + '/' + file_name2 + '.woff2')
            except Exception as e:
                pass
            continue
        # 生成字体样式
        helper.font_to_css(file_css, font_family, file_list)

    print('字体转标题网页字体完成！')