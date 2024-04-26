import glob
import os
import re
import regex

def get_params_with_parentheses(target: str, param: str) -> list[list]: # type: ignore
    """
    `param: xxx {yyy}` 形式の要素を、list形式（[[xxx, {yyy}], ...]）で取得する
    """
    # 下記正規表現の参考 : https://ja.stackoverflow.com/a/32941
    pattern: str = param + r"\s*:\s*([^\{\}\s]+)\s*(?<rec>\{(?:[^\{\}]+|(?&rec))*\})"
    return regex.findall(pattern, target)


def get_includes(target: str, base_dir: str) -> list[str]: # type: ignore
    result: list[str] = []
    paths: list[str] = [
        re.sub(r"(.*)view$", r"\1view.lkml", base_dir + v)
        for v in re.findall(r"(?:\s+|^)include\s*:\s*[\'\"]([^\'\"]+)[\'\"]", target)
    ]
    if len(paths) > 0:
        for path in paths:
            for p in glob.glob(path, recursive=True):
                result.append(p)
                with open(p, mode="r") as f:
                    result.extend(get_includes(target=f.read(), base_dir=base_dir))

    return result


def get_relative_path(path: str, base_dir: str) -> str:
    return os.path.relpath(path=path, start=base_dir)
