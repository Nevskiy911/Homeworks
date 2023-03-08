import os
import re
import sys
import shutil


images_format = [".jpg", ".jpeg", ".png", ".svg"]
documents_format = [".txt", ".doc", ".docx", ".xlsx", ".pptx" ".pdf"]
audio_format = [".mp3", ".ogg", ".wav", ".amr"]
video_format = [".avi", ".mp4", ".mov", ".mkv"]
archives_format = [".zip", ".gz", ".tar"]


def normalize(name: str) -> str:
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}
    for c, l in zip(list(CYRILLIC_SYMBOLS), TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    trans_name = name.translate(TRANS)
    trans_name = re.sub(r'\W', '_', trans_name)
    return trans_name


def sort(folder):
    files = os.listdir(folder)
    for items in files:
        format = items.split(".")
        if len(format) > 1 and format[1].lower() in images_format:
            file = folder + "/" + items
            new_path = folder + "/images/" + items
            shutil.move(file, new_path)
        elif len(format) > 1 and format[1].lower() in video_format:
            file = folder + "/" + items
            new_path = folder + "/video/" + items
            shutil.move(file, new_path)
        elif len(format) > 1 and format[1].lower() in documents_format:
            file = folder + "/" + items
            new_path = folder + "/documents/" + items
            shutil.move(file, new_path)
        elif len(format) > 1 and format[1].lower() in audio_format:
            file = folder + "/" + items
            new_path = folder + "/audio/" + items
            shutil.move(file, new_path)
        elif len(format) > 1 and format[1].lower() in archives_format:
            file = folder + "/" + items
            new_path = folder + "/archives/" 
            shutil.unpack_archive(new_path[items])
        else:
            file = folder + "/" + items
            new_path = folder + "/unknown/" + items
            shutil.move(file, new_path)


if __name__ == '__main__':
    folder = input('Folder:')
