import os
import json
from fontbro import Font
from app import helper

# 生成字体 json 文件
def fonts_json(lang_dir = None):
    font_id = ''
    fonts_data_kv = {}
    fonts_data = []
    font_dirs = helper.read_font_dirs(lang_dir)

    for font_dir in font_dirs:
        font_path = font_dir['font_path']
        about_file = font_path + '/about.json'
        json_data = []

        # 读取 JSON 文件
        json_data = helper.read_json_file(about_file)

        if json_data.get('id') is None:
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
                font_weight = font.get_weight()
                font_style = 'normal' if not font.get_style_flag(Font.STYLE_FLAG_ITALIC) else 'italic'
                file_name2, file_ext = os.path.splitext(file_name)
                file_list.append({'file_name': file_name, 'font_weight_name': font_weight['name'], 'font_weight_value': font_weight['value'], 'font_style': font_style})

            json_data['file_list'] = file_list

            if not json_data.__contains__('family'):
                json_data['family'] = font_names['family_name'] if font_names.__contains__('family_name') else font_names['full_name']

            font_id = json_data['family'].replace(' ', '').lower()

            json_data['id'] = font_id
            json_data['file_path'] = font_path
            json_data['language'] = font_dir['lang_dir']
            json_data['title'] = json_data['title'] if json_data.__contains__('title') else font_names['family_name']
            json_data['source_url'] = json_data['source_url'] if json_data.__contains__('source_url') else ''
            json_data['version'] = font_names['version'] if font_names.__contains__('version') else ''
            json_data['description'] = font_names['description'] if font_names.__contains__('description') else ''
            json_data['vendor_url'] = font_names['vendor_url'] if font_names.__contains__('vendor_url') else ''
            json_data['designer'] = font_names['designer'] if font_names.__contains__('designer') else ''
            json_data['designer_url'] = font_names['designer_url'] if font_names.__contains__('designer_url') else ''
            json_data['copyright'] = font_names['copyright_notice'] if font_names.__contains__('copyright_notice') else ''
            json_data['license_url'] = font_names['license_info_url'] if font_names.__contains__('license_info_url') else ''
            json_data['license_description'] = font_names['license_description'] if font_names.__contains__('license_description') else ''
            json_data['names'] = font_names

            helper.write_json_file(font_path + '/' + 'about.json', json_data)
        else:
            font_id = json_data['id']

        del json_data['names'],json_data['version'],json_data['description'],json_data['vendor_url'],json_data['designer'],json_data['designer_url'],json_data['copyright'],json_data['license_url'],json_data['license_description']
        fonts_data.append(json_data)
        fonts_data_kv[font_id] = json_data

    if lang_dir:
        lang_dir = '-' + lang_dir
    else:
        lang_dir = ''

    helper.write_json_file('fonts' + lang_dir + '.json', fonts_data)
    helper.write_json_file('fonts' + lang_dir + '-kv.json', fonts_data_kv)

    print('写入[fonts' + lang_dir + '.json]文件完成...')