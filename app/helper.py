from fontbro import Font
import os

# 生成web字体
def font_to_woff2(text: str, fontpath: str, savepath: str):
    font = Font(fontpath)

    if text:
        font.subset(text=text)

    return font.save_as_woff2(filepath=savepath, overwrite=True)


# 写入文件内容
def write_file(content: str, filepath: str):
    f = open(filepath, 'w')
    f.write(content)
    f.close()

# 读取文件内容
def read_file(filepath: str):
    f = open(filepath, 'r')
    content = f.read()
    f.close()

    return content

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
        "thin": "100"
    }

    weight = font_weights.get(name, None)

    return weight if not weight is None else "400"


# 生成字体样式
def font_to_css(fontfamily: str, filenames: str, filecss: str):
    csscode = ""

    for filename in filenames:
        weight = filename.split('-')

        if len(weight) > 1:
            weight = weight[1].lower()
        else:
            weight = "regular"

        weight = font_weight(weight)

        csscode += "@font-face{font-family:'" + fontfamily + "';src:url('" + filename + ".woff2') format('woff2');font-weight:" + weight + ";font-style:normal;font-display:swap;}"

        write_file(csscode, filecss)


# 返回字体列表，对象属性形式。
def font_list():
    items = []
    dirs = os.listdir("fonts/")

    for dirname in dirs:
        files = os.listdir("fonts/" + dirname)
        for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext == '.txt':
                items.append({'family':dirname, 'title': os.path.splitext(filename)[0]})

    return items


# 返回字体列表，键值对形式。格式：{字体名称:字体标题,字体名称2:字体标题2}
def font_list_kv():
    items = {}
    dirs = os.listdir("fonts/")

    for dirname in dirs:
        files = os.listdir("fonts/" + dirname)
        for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext == '.txt':
                items[dirname] = os.path.splitext(filename)[0]

    return items


# 返回字体标题
def font_title(name: str):
    fonts = font_list_kv()

    return fonts.get(name, None)