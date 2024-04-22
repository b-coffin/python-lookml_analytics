import csv
import datetime
import glob
import jinja2
import json
import os
import polars
import re

from typing import Tuple
from zoneinfo import ZoneInfo

COLOR_BLUE = "blue"
COLOR_YELLOW = "yellow"
COLOR_GREEN = "green"

def print_with_color(text: str, color: str) -> None:
    if color == COLOR_BLUE:
        print(f"\033[34m{text}\033[0m")
    elif color == COLOR_GREEN:
        print(f"\033[32m{text}\033[0m")
    elif color == COLOR_YELLOW:
        print(f"\033[33m{text}\033[0m")
    else:
        print(text)


# jinja2のテンプレートを読み込む
# 参考: https://qiita.com/simonritchie/items/cc2021ac6860e92de25d
def get_text_used_jinja2template(template_path: str, render_content) -> str:
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=os.path.dirname(template_path), encoding="utf8"))
    template = env.get_template(os.path.basename(template_path))
    return template.render(render_content)


# Terminal上で必要になるエスケープ処理を入れる
def get_escapedtext_forcommand(text: str) -> str:
    return text.replace(" ", "\\ ").replace("[", "\\[").replace("]", "\\]").replace("(", "\\(").replace(")", "\\)").replace("&", "\\&")


def get_filename_withoutextension(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]


def get_basefilename(path: str) -> str:
    return os.path.basename(path)


def get_nowdatetime():
    """
    現在の日時を YYYYMMDDHHMMSS の形式で返す
    """
    return datetime.datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y%m%d%H%M%S")


# 正規表現

def is_contain_allwords(text: str, words: list[str]) -> bool: # type: ignore
    """
    list形式で渡された文字列全てを含んでいるかどうかを判定
    """
    return True if re.search(rf"^{''.join(list(map(lambda x: f'(?=.*{x})', words)))}.*$", text) else False


def get_filenames(path: str, extensions: list[str], words: list[str]) -> list[str]: # type: ignore
    """
    path配下のファイルの中で、list形式で渡された文字列全てを含んでいるファイル名を返す
    """
    result_list = []
    cleased_words = list(filter(None, words)) # None要素を削除
    for ex in extensions:
        paths = glob.glob(f"{path}/**/*.{ex}", recursive=True)
        if len(cleased_words) == 0:
            result_list.extend(paths)
        else:
            result_list.extend([p for p in paths if is_contain_allwords(str(p), cleased_words)])
    return result_list


# ファイルの読み込み

def read_jsonfile(path: str) -> dict:
    return json.load(open(path, "r"))


# ファイルの書き込み

def write_csv(path: str, list: list[list]|list[Tuple]) -> None: # type: ignore
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        writer = csv.writer(f)
        writer.writerows(list)


def write_jsonl_file(path: str, jsons: list[dict]) -> None: # type: ignore
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        for j in jsons:
            f.writelines(f"{json.dumps(j)}\n")


def write_text_file(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def write_df_to_csv(path: str, df: polars.DataFrame) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.write_csv(path, separator=",")


def write_dicts_to_csv(path: str, dicts: list[dict]) -> None: # type: ignore
    write_df_to_csv(path, polars.DataFrame(dicts))
