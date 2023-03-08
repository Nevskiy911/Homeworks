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
    "archives": [".zip", ".gz", ".tar"],
    "unknown": []
}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t",
                "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")


TRANS = {}
for c, l in zip(list(CYRILLIC_SYMBOLS), TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str:
    trans_name = name.translate(TRANS)
    trans_name = re.sub(r'\W', '_', trans_name)
    return trans_name


def move_file(file:Path, root_dir:Path, category:str):
    target_folder = root_dir / category
    
    if not target_folder.exists():
        target_folder.mkdir()
    
    file.replace(target_folder / f"{normalize(file.stem)}{file.suffix}")


def get_category(item: Path):
    for category, exts in file_ext.items():
        if item.suffix.lower() in exts:
            return category
    return "unknown"


def rm_dir(dir:Path):
    try:
        dir.rmdir()
    except OSError as e:
        print(e)


def sort_dir(sub_dir:Path, root_dir: Path):
    for item in list(sub_dir.glob('**/*'))[::-1]:
        if item.is_file():
            category = get_category(item)
            move_file(item, root_dir, category)
        else:
            rm_dir(item)


def sort_func(path_dir:Path):

    for item in [p for p in path_dir.glob('*') if p.name.lower() not in file_ext.keys()][::-1]:
        if item.is_dir():
            sort_dir(item, path_dir)
            rm_dir(item)
        else:
            category = get_category(item)
            move_file(item, path_dir, category)


def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        print("Type path to folder as parameter on call script")
        return None
    if not Path(path).exists():
        print('!!! The directory not found')
        return None
    
    sort_func(path)
    print('OK. Process has been finished!')


if __name__ == "__main__":
    main()