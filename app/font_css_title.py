import os
from app import helper

def font_css_title():

    dirs = os.listdir("fonts/")

    for dirname in dirs:
        csscode = ""

        save_path = "css/title/" + dirname + "/"

        css_file_name = save_path + dirname + ".css"

        if os.path.exists(css_file_name):
            continue

        files = os.listdir("fonts/" + dirname)

        for filename in files:
            ext = os.path.splitext(filename)[1]

            if ext == '.ttf' or ext == '.otf':
                font_title = helper.font_title(dirname)

                filename2 = filename.replace(".ttf", "").replace(".otf", "")

                helper.font_to_woff2(font_title, "fonts/" + dirname + "/" + filename, save_path + filename2 + ".woff2")

                weight = filename2.split('-')

                if len(weight) > 1:
                    weight = weight[1].lower()
                else:
                    weight = "regular"

                weight = helper.font_weight(weight)

                csscode += "@font-face{font-family:'" + dirname + "';src:url('" + filename2 + ".woff2') format('woff2');font-weight:" + weight + ";font-style:normal;font-display:swap;}"

        helper.write_file(csscode, css_file_name)