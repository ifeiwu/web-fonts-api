import os
import json
from sqlite_utils import Database
from app import helper

def font_css_words():
    db = Database('fonts.db')
    words = {"3500":"zh-cn", "5000":"zh-cn", "7000":"zh-cn"}

    for number, lang in words.items():
        fonts = db['fonts'].rows
        for font in fonts:
            if not font['language'] == lang:
                continue

            font_id = font['id']
            file_path = font['file_path']
            font_family = font['family']
            file_list = json.loads(font['file_list'])

            save_path = 'css/' + number + '/' + lang + '/' + font_id

            file_css = save_path + '/' + font_id + '.css'

            if os.path.exists(file_css):
                continue

            # 读取文件内容
            content = helper.read_file('words/' + number + '_' + lang + '.txt')

            for file in file_list:
                try:
                    file_name = file['file_name']
                    file_name2 = os.path.splitext(file_name)[0]
                    # 生成web字体
                    helper.font_to_woff2(content, file_path + '/' + file_name, save_path + '/' + file_name2 + '.woff2')
                except Exception as e:
                    pass
                continue
            # 生成字体样式
            helper.font_to_css(file_css, font_family, file_list)

    print('字体转指定文字完成！')