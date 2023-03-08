import os
import re
import shutil
import sys
from pathlib import Path

file_ext = {
    "images": [".jpg", ".jpeg", ".png", ".svg"],
    "documents": [".txt", ".doc", ".docx", ".xlsx", ".pptx", ".pdf"], #".odt", ".odf"]
    "audio": [".mp3", ".ogg", ".wav", ".amr"],
    "video": [".avi", ".mp4", ".mov", ".mkv"],
    "archives": [".zip", ".gz", ".tar"]
}


def normalize(name: str) -> str:
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t",
                   "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}
    for c, l in zip(list(CYRILLIC_SYMBOLS), TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    trans_name = name.translate(TRANS)
    trans_name = re.sub(r'\W', '_', trans_name)
    return trans_name


def move_file(path_dir, p_file, cat, num):
    shutil.move(p_file, Path(path_dir) / cat / f'{Path(p_file).name.split(Path(p_file).suffix)[0]}_'
                                               f'{num}{Path(p_file).suffix}')
    print(f"Мaybe a duplicate: {p_file.name}")


def sort_func(path_dir):
    dir_path = []

    for root, dirs, files in os.walk(path_dir):
        for d in dirs:
            dir_path.append(os.path.join(root, d))
        for num, file in enumerate(files):
            p_file = Path(root) / file
            name_normalize = f"{normalize(p_file.name[0:-len(p_file.suffix)])}{p_file.suffix}"
            p_file.rename(Path(root) / name_normalize)
            p_file = Path(root) / name_normalize
            for cat in file_ext:
                if p_file.suffix.lower() in file_ext[cat]:
                    (Path(path_dir) / cat).mkdir(exist_ok=True)
                    try:
                        if not (Path(path_dir) / cat / Path(p_file).name).exists():
                            shutil.move(p_file, Path(path_dir) / cat / Path(p_file).name)
                            continue
                        else:
                            move_file(path_dir, p_file, cat, num)
                            continue
                    except FileExistsError:
                        move_file(path_dir, p_file, cat, num)
                        continue
            if p_file.exists():
                (Path(path_dir) / "unknown").mkdir(exist_ok=True)
                try:
                    shutil.move(p_file, Path(path_dir) / "unknown" / Path(p_file).name)
                except FileExistsError:
                    move_file(path_dir, p_file, "unknown", num)

    for dir_p in dir_path:
        shutil.rmtree(dir_p)


if __name__ == "__main__":
    try:
        path = sys.argv[1].replace("'", "").replace('"', '')
    except IndexError:
        path = input('>>> Enter your way to the directory: ').replace("'", "").replace('"', '')
    if not Path(path).exists():
        print('!!! The directory not found')
    else:
        sort_func(path)
    print('OK. Process has been finished!')