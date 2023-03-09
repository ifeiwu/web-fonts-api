import os


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
    items = {}
    dirs = os.listdir("fonts/")

    for dirname in dirs:
        files = os.listdir("fonts/" + dirname)
        for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext == '.txt':
                items[dirname] = os.path.splitext(filename)[0]

    return items



def font_title(name):
    fonts = font_list()

    return fonts.get(name, None)