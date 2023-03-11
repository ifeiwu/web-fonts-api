import os
import random
import time
import datetime
from app import helper

def font_css_text(words, dirname):

    temp_rand = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')

    file_list = []

    font_list = os.listdir("fonts/" + dirname)

    for filename in font_list:
        ext = os.path.splitext(filename)[1]

        if ext == '.ttf' or ext == '.otf':
            filename2 = filename.replace(".ttf", "").replace(".otf", "")

            saved_path = helper.font_to_woff2(words, "fonts/" + dirname + "/" + filename, "temp/" + temp_rand + '/' + filename2 + ".woff2")

            file_list.append(saved_path)

    return file_list