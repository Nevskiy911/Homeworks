import os
import re
import sys
from pathlib import Path

new_dir_dct = {"images": [".jpg", ".jpeg", ".png", ".svg"], "documents": [".txt", ".doc", ".docx", ".xlsx", ".pptx", ".pdf"], "audio": [
    ".mp3", ".ogg", ".wav", ".amr"], "video": [".avi", ".mp4", ".mov", ".mkv"], "archives": [".zip", ".gz", ".tar"], "unknown": []}


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


def sort_func(path_dir):
    cur_dir = Path(path_dir)
    dir_path = []

    for root, dirs, files in os.walk(path_dir):
        for d in dirs:
            dir_path.append(os.path.join(root, d))
        for file in files:
            p_file = Path(root) / file
            name_normalize = f"{normalize(p_file.name[0:-len(p_file.suffix)])}{p_file.suffix}"
            p_file.rename(Path(root) / name_normalize)
            p_file = Path(root) / name_normalize
            for suff in new_dir_dct:
                if p_file.suffix.lower() in new_dir_dct[suff]:
                    dir_img = cur_dir / suff
                    dir_img.mkdir(exist_ok=True)
                    try:
                        p_file.rename(dir_img.joinpath(p_file.name))
                    except FileExistsError:
                        p_file.rename(dir_img.joinpath(
                            f'{p_file.name.split(".")[0]}_c{p_file.suffix}'))
                        print(f"Мaybe a duplicate: {p_file.name}")
                elif p_file.suffix.lower() in new_dir_dct[suff]:
                    unknown_suff = "unknown"
                    dir_img = cur_dir / unknown_suff
                    dir_img.mkdir(exist_ok=True)
                    try:
                        p_file.rename(dir_img.joinpath(p_file.name))
                    except FileExistsError:
                        p_file.rename(dir_img.joinpath(
                            f'{p_file.name.split(".")[0]}_c{p_file.suffix}'))
                        print(f"Мaybe a duplicate: {p_file.name}")

    for dir_p in reversed(dir_path):
        if os.path.split(dir_p)[1] in new_dir_dct or os.stat(dir_p).st_size != 0:
            continue
        else:
            try:
                os.rmdir(dir_p)
            except OSError:
                print("System file")


if __name__ == "__main__":
    path_dir = sys.argv[1]
    sort_func(path_dir)
