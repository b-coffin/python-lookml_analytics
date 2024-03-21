import os

import pandas as pd

from getfields import get_fieldnames

def main():

    # 対象ファイルをキーボード入力から取得
    filename1 = input("Input file name 1 (default: sample.txt) : ") or "sample.txt"
    filename2 = input("Input file name 2 (default: sample_forcomp.txt) : ") or "sample_forcomp.txt"

    list_1 = []
    list_2 = []

    with open(os.path.join(os.path.dirname(__file__), "input", filename1), mode="r") as f:
        data = f.read()
        list_1 = get_fieldnames(data)

    with open(os.path.join(os.path.dirname(__file__), "input", filename2), mode="r") as f:
        data = f.read()
        list_2 = get_fieldnames(data)

    merged_df = pd.merge(pd.DataFrame({"fname": list_1}), pd.DataFrame({"fname": list_2}), on="fname", how="outer", indicator="indicator")

    result = {filename1: [], filename2: []}
    for row in merged_df.itertuples():
        if row.indicator == "both":
            result[filename1].append(row.fname)
            result[filename2].append(row.fname)
        elif row.indicator == "left_only":
            result[filename1].append(row.fname)
            result[filename2].append("")
        elif row.indicator == "right_only":
            result[filename1].append("")
            result[filename2].append(row.fname)

    # csvに出力
    pd.DataFrame(result).to_csv(os.path.join(os.path.dirname(__file__), "output", f"compare_{filename1}_{filename2}.csv"), index=False)
    print("...output Done")

# メイン
if __name__ == "__main__":
    main()
