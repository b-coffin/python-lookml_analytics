# LookMLのviewファイルから、field名を取得する

import csv
import numpy
import os
import re

def main():

    # 対象ファイル名をキーボード入力から取得
    filename = input("Input file name (default: sample.txt) : ") or "sample.txt"

    with open(os.path.join(os.path.dirname(__file__), "input", filename), mode="r") as f:
        data = f.read()

        fields = get_fieldnames(data)
        result = numpy.array([fields]).T # 転置

        # 書き込み
        with open(os.path.join(os.path.dirname(__file__), "output", f"{filename}.csv"), mode="w") as output:
            writer = csv.writer(output)
            writer.writerows(result)

def get_fieldnames(txt):
    return re.findall(r"(?:dimension|dimension_group|filter|measure|parameter):\s*([^\s{]+?)\s*{", txt)

# メイン
if __name__ == "__main__":
    main()

