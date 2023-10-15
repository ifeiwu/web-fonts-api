import os
import json
from fontbro import Font
from app import helper
from sqlite_utils import Database

# 所有字体导入数据库
def fonts_db():
    db = Database('fonts.db', recreate=True)
    font_id = ''
    font_ids = []
    fonts_data = []
    font_dirs = helper.read_font_dirs()

    for font_dir in font_dirs:
        font_path = font_dir['font_path']
        if len(os.listdir(font_path)) == 0:
            print(font_path)
            continue
        about_file = font_path + '/about.json'
        # 读取 JSON 文件
        about_data = helper.read_json_file(about_file)

        if about_data.get('id') is None:
            # 记录多重字体
            file_list = []
            # 所有字体文件
            font_files = helper.read_font_files(font_path)

            # 获取第一个字体信息
            if len(font_files):
                first_name = font_files[0]
                font = Font(font_path + '/' + first_name)
                font_names = font.get_names()

            # 多重字体列表
            for file_name in font_files:
                font = Font(font_path + '/' + file_name)
                font_style = 'normal' if not font.get_style_flag(Font.STYLE_FLAG_ITALIC) else 'italic'
                file_name2, file_ext = os.path.splitext(file_name)

                file_name3 = file_name2.split('-', 1)
                font_weight_name = 'Regular'
                if len(file_name3) >= 2:
                    font_weight_name = file_name3[len(file_name3) - 1]

                font_weight_value = helper.font_weight(font_weight_name)

                file_list.append({'file_name': file_name, 'font_weight_name': font_weight_name, 'font_weight_value': font_weight_value, 'font_style': font_style})

            about_data['file_list'] = file_list

            if not about_data.__contains__('family'):
                about_data['family'] = font_names['family_name'] if font_names.__contains__('family_name') else font_names['full_name']

            font_id = about_data['family'].strip().replace(' ', '-').lower()

            about_data['id'] = font_id
            about_data['file_path'] = font_path
            about_data['language'] = font_dir['lang_dir']
            about_data['title'] = about_data['title'] if about_data.__contains__('title') else font_names['family_name']
            about_data['source_url'] = about_data['source_url'] if about_data.__contains__('source_url') else ''
            about_data['version'] = font_names['version'] if font_names.__contains__('version') else ''
            about_data['description'] = font_names['description'] if font_names.__contains__('description') else ''
            about_data['vendor_url'] = font_names['vendor_url'] if font_names.__contains__('vendor_url') else ''
            about_data['designer'] = font_names['designer'] if font_names.__contains__('designer') else ''
            about_data['designer_url'] = font_names['designer_url'] if font_names.__contains__('designer_url') else ''
            about_data['copyright'] = font_names['copyright_notice'] if font_names.__contains__('copyright_notice') else ''
            about_data['license_url'] = font_names['license_info_url'] if font_names.__contains__('license_info_url') else ''
            about_data['license_description'] = font_names['license_description'] if font_names.__contains__('license_description') else ''
            about_data['names'] = font_names

            helper.write_json_file(font_path + '/' + 'about.json', about_data)
        else:
            font_id = about_data['id']

        del about_data['names'],about_data['version'],about_data['description'],about_data['vendor_url'],about_data['designer'],about_data['designer_url'],about_data['copyright'],about_data['license_url'],about_data['license_description']
        # print('---'+font_id+'--'+about_data['file_path'])
        if helper.is_in_array(font_id, font_ids):
            print('重复的字体id：' + font_id + ' -> ' + font_path)
        font_ids.append(font_id)
        fonts_data.append(about_data)

    db['fonts'].insert_all(fonts_data, pk="id")
    db["fonts"].create_index(["family"], unique=True)

    print('导入[fonts.db]数据库完成.')