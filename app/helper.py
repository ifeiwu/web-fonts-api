from fontbro import Font
import os


def font_to_woff2(text: str, fontpath: str, savepath: str):
    font = Font(fontpath)

    if text:
        font.subset(text=text)

    return font.save_as_woff2(filepath=savepath, overwrite=True)


def write_file(content: str, filepath: str):
    cssfile = open(filepath, 'w')
    cssfile.write(content)
    cssfile.close()


def remove_empty_dir(dir):
    for root, dirs, files in os.walk(dir):
        if not os.listdir(root):
            os.rmdir(root)


def font_weight(name):

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
        "thin": "100"
    }

    weight = font_weights.get(name, None)

    return weight if not weight is None else "400"


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


def font_title(name: str):
    fonts = font_list_kv()

    return fonts.get(name, None)