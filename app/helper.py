from starlette.responses import FileResponse
from starlette.background import BackgroundTask
from sqlite_utils import Database
from fontbro import Font
from typing import Union
import requests
import zipfile
import shutil
import json
import glob
import os


# 生成web字体
def font_to_woff2(text: str, font_path: str, save_path: str):
    saved_path = ''

    try:
        font = Font(font_path)
        if text:
            font.subset(text=text)
        #else:
            # 常用 unicode 编码表：https://www.shubang.net/unicode/
            # 常用汉字区（4E00-62FF），次常用汉字区（6300-77FF），非常用汉字区（7800-8CFF），未分类汉字区（8D00-9FFF）。中文繁体字符集（3400-4DBF）
            # 中日韩统一表意文字字符 4E00-9FFF：https://www.unicode.org/charts/PDF/U4E00.pdf
            #font.subset(unicodes="4E00-9FFF 1D400−1D7FF 2190−21FF 2200−22FF 2460−24FF 2500−257F 2580−259F 25A0−25FF 2000−206F AC00−D7AF 20A0−20CF 0E00−0E7F 3000−303F 3200−32FF")

        saved_path = font.save_as_woff2(filepath=save_path, overwrite=True)
    except Exception as err:
        print(f"{font_path} => {save_path}, Error {err=}")
    else:
        font.close()

    return saved_path


# 写入文件内容
def write_file(content: str, filepath: str):
    try:
        f = open(filepath, 'w')
        f.write(content)
    except Exception as err:
        print(f"{filepath}, Error {err=}")
    else:
        f.close()


# 读取文件内容
def read_file(filepath: str):
    f = open(filepath, 'r')
    content = f.read()
    f.close()

    return content


# 读取所有字体文件
def read_font_files(path: str):
    font_files = []

    files = os.listdir(path)

    for font_file in files:
        if os.path.isfile(path + '/' + font_file):
            ext = os.path.splitext(font_file)[1]
            if ext == '.ttf' or ext == '.otf':
                font_files.append(font_file)

    return font_files


# 读取css所有字体文件
def read_css_files(path: str):
    font_files = []

    files = os.listdir(path)

    for font_file in files:
        filename = path + '/' + font_file
        if os.path.isfile(filename):
            font_files.append(filename)

    return font_files


# 读取 json 文件
def read_json_file(filepath: str):
    json_data = {}

    if os.path.isfile(filepath) and os.path.getsize(filepath):
        with open(filepath, 'r') as json_file:
            json_data = json.load(json_file)

    return json_data


# 写入 json 文件
def write_json_file(filepath: str, json_data: Union[dict, list]):
    json_str = json.dumps(json_data, sort_keys=True, ensure_ascii=False, indent = 4)
    with open(filepath, 'w', encoding='utf-8') as jsonfile:
        jsonfile.write(json_str)


# 读取字体目录列表
def read_font_dirs(lang_dir = None):
    _font_dirs = []

    if lang_dir == None:
        lang_dirs = os.listdir('fonts')
        for lang_dir in lang_dirs:
            read_font_dirs2(lang_dir, _font_dirs)
    else:
        read_font_dirs2(lang_dir, _font_dirs)

    return _font_dirs

# 读取指定语言字体目录列表
def read_font_dirs2(lang_dir: str, _font_dirs = []):
    lang_path = 'fonts/' + lang_dir
    font_dirs = os.listdir(lang_path)

    for font_dir in font_dirs:
        font_path = lang_path + '/' + font_dir
        if os.path.isdir(font_path):
            _font_dirs.append({'lang_dir': lang_dir, 'font_dir': font_dir, 'font_path': font_path})

    return _font_dirs


# 删除空目录
def remove_empty_dir(dir: str):
    for root, dirs, files in os.walk(dir):
        if not os.listdir(root):
            os.rmdir(root)


# 返回字体粗细程度
def font_weight(name: str):
    font_weights = {
        "heavy": "900",
        "black": "900",
        "extrabold": "800",
        "bold": "700",
        "semibold": "600",
        "demibold": "600",
        "medium": "500",
        "light": "300",
        "extralight": "200",
        "ultralight": "200",
        "thin": "100",

        "heavyitalic": "900",
        "blackitalic": "900",
        "extrabolditalic": "800",
        "bolditalic": "700",
        "semibolditalic": "600",
        "demibolditalic": "600",
        "mediumitalic": "500",
        "lightitalic": "300",
        "extralightitalic": "200",
        "ultralightitalic": "200",
        "thinitalic": "100"
    }

    weight = font_weights.get(name.lower(), None)

    return weight if not weight is None else "400"


# 生成字体样式css文件
def font_to_css(file_css: str, family: str, file_list: list):
    css_code = ''

    for file in file_list:
        file_name = file['file_name']
        file_name2 = os.path.splitext(file_name)[0]
        weight = file['font_weight_value']
        style = file['font_style']
        css_code += "@font-face{font-family:'" + family + "';src:url('" + file_name2 + ".woff2') format('woff2');font-weight:" + str(weight) + ";font-style:" + style + ";font-display:swap;}"

    write_file(css_code, file_css)


# 返回字体列表，键值对形式。格式：[{字体id:字体对象}]
def font_list(type = None, lang = None, keyword = None, orderby = None, offset = None, limit = None):
    db = Database('fonts.db')
    select = 'id, title, family, language, source_url'

    # 搜索所有字体
    if lang == None and keyword == None:
        rows = db['fonts'].rows_where(select=select, order_by=orderby, offset=offset, limit=limit)
        count = db['fonts'].count
    # 搜索指定语言的字体
    elif lang != None and keyword == None:
        rows = db['fonts'].rows_where('language = ?', [lang], select=select, order_by=orderby, offset=offset, limit=limit)
        count = db['fonts'].count_where('language = ?', [lang])
    # 搜索指定语言和关键词的字体
    elif lang != None and keyword != None:
        rows = db['fonts'].rows_where('language = ? and (title like ? or family like ?)', [lang, '%' + keyword + '%', '%' + keyword + '%'], select=select, order_by=orderby, offset=offset, limit=limit)
        count = db['fonts'].count_where('language = ? and (title like ? or family like ?)', [lang, '%' + keyword + '%', '%' + keyword + '%'])
    # 搜索所有关键词的字体
    elif keyword != None:
        rows = db['fonts'].rows_where('title like ? or family like ?', ['%' + keyword + '%', '%' + keyword + '%'], select=select, order_by=orderby, offset=offset, limit=limit)
        count = db['fonts'].count_where('title like ? or family like ?', ['%' + keyword + '%', '%' + keyword + '%'])

    # 数据结构是对象或数组
    if type == 'array':
        fonts = []
        for row in rows:
            fonts.append(row)
    else:
        fonts = {}
        for row in rows:
            fonts[row['id']] = row

    return {'count': count,'fonts': fonts}


# 通过id或family字段查找一个字体信息
def font_one(id = None, family = None):
    db = Database('fonts.db')
    select = 'id, title, family, language, source_url'
    font = {}

    if id != None:
        rows = db['fonts'].rows_where('id = ?', [id], select=select, offset=0, limit=1)
    elif family != None:
        rows = db['fonts'].rows_where('family = ?', [family], select=select, offset=0, limit=1)

    for row in rows:
        font = row

    return font


# 文件下载
def download(filename: str, action = None):
    if action == 'remove':
        remove_empty_dir('temp/')
        return FileResponse(filename, background=BackgroundTask(lambda: os.remove(filename)))
    else:
        return FileResponse(filename)


# fontsource.org 接口下载谷歌字体源文件到目录 fonts/en/
def download_google_fonts():
    response = requests.get('https://api.fontsource.org/fontlist')
    if response.status_code == 200:
        font_ids = json.loads(response.text)
        for id in font_ids:
            save_path = 'fonts/en/' + id
            if not os.path.exists(save_path):
                os.makedirs(save_path)
                response2 = requests.get('https://api.fontsource.org/v1/fonts/' + id)
                if response2.status_code == 200:
                    font_info = json.loads(response2.text)
                    subsets = font_info['subsets']

                    # 不下载的字体
#                     ignore = False
#                     ignore_fonts = ['chinese-simplified', 'chinese-traditional', 'chinese-hongkong', 'japanese', 'korean', 'arabic', 'cyrillic', 'devanagari', 'greek', 'gujarati', 'gurmukhi', 'hebrew', 'kannada', 'khmer', 'malayalam', 'myanmar', 'oriya', 'sinhala', 'tamil', 'telugu', 'thai', 'tibetan', 'duployan', 'bengali', 'ethiopic', 'symbols', 'emoji', 'signwriting']
#                     for ignore_font in ignore_fonts:
#                         if is_in_array(ignore_font, subsets):
#                             ignore = True
#                             break
#                     if ignore == True:
#                         continue

                    # 不下载的分类
                    if font_info['category'] == 'icons':
                        continue

                    # 只下载 latin 和 latin-ext
                    if len(subsets) > 2:
                        continue
                    if len(subsets) == 1 and subsets[0] != 'latin':
                        continue
                    if len(subsets) == 2 and (subsets[0] != 'latin' or subsets[1] != 'latin-ext'):
                        continue

                    # 从谷歌网站下载字体并解压
                    family = font_info['family']
                    response3 = requests.get('https://fonts.google.com/download?family=' + family, allow_redirects=True)
                    if response3.status_code == 404:
                        continue
                    # 解压字体包
                    zipname = save_path + '/' + family + '.zip'
                    if open(zipname, 'wb').write(response3.content):
                        zipfiles = zipfile.ZipFile(zipname)
                        for file in zipfiles.namelist():
                            zipfiles.extract(file, save_path)
                        zipfiles.close()
                        os.remove(zipname)
                        # 可变字体处理
                        if os.path.isdir(save_path + '/static'):
                            print(save_path + '/static')
                            remove_files_by_name(save_path, '*.ttf') # 删除可变字体
                            move_files(save_path + '/static', save_path) # 移动静态字体到上级目录
                            remove_empty_dir(save_path + '/static')
                        # 删除斜体字体
                        if len(font_info['weights']) > 1:
                            remove_files_by_name(save_path, '*Italic.ttf')
                        # 保存字体信息
                        write_json_file(save_path + '/fontsource.json', font_info)

    else:
        print("请求失败!")

# 判断字符串是否在数组中
def is_in_array(target, array):
    for item in array:
        if item == target:
            return True
    return False


# 移动文件
def move_files(old_path, new_path):
    filelist = os.listdir(old_path)
    for file in filelist:
        src = os.path.join(old_path, file)
        dst = os.path.join(new_path, file)
        shutil.move(src, dst)

# 删除目录下指定文件名
def remove_files_by_name(path, name = '*.txt'):
    for file in glob.glob(os.path.join(path, name)):
         os.remove(file)