import re
import regex

def get_params_with_parentheses(target: str, param: str) -> list[list]: # type: ignore
    """
    `param: xxx {yyy}` 形式の要素を、list形式（[[xxx, {yyy}], ...]）で取得する
    """
    # 下記正規表現の参考 : https://ja.stackoverflow.com/a/32941
    pattern: str = param + r"\s*:\s*([^\{\}\s]+)\s*(?<rec>\{(?:[^\{\}]+|(?&rec))*\})"
    return regex.findall(pattern, target)


def get_includes(target: str) -> list[str]: # type: ignore
    return re.findall(r"(?:\s+|^)include\s*:\s*[\'\"]([^\'\"]+)[\'\"]", target)


def get_relative_path(path: str, base_dir: str) -> str:
    return re.sub(rf"^{base_dir}(.+)", r"\1", path)


def get_absolute_path(relative_path: str, base_dir: str) -> str:
    return base_dir + relative_path