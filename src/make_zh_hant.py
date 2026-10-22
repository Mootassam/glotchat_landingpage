"""繁體中文 (Taiwan / Hong Kong) site text, generated from the 简体 text:
    python src/make_zh_hant.py      then   python src/build.py

OpenCC "s2twp" converts characters AND Taiwan wording (软件→軟體, 内存→記憶體, 视频→影片); the fixes below
cover chat-app words it leaves mainland-style, and say honestly that the app's own interface is 简体中文.
Edit zh.yaml (never zh-hant.yaml by hand), then run this again.
"""
import os
import re

from opencc import OpenCC        # pip install opencc-python-reimplemented

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "content", "zh.yaml")
DST = os.path.join(HERE, "content", "zh-hant.yaml")

FIXES = [
    ("賬", "帳"),                              # 帳號 / 帳戶 (Taiwan / Hong Kong)
    ("消息", "訊息"),                          # a chat message
    ("騷擾資訊", "騷擾訊息"), ("垃圾資訊", "垃圾訊息"),
    ("二維碼", "QR Code"),
    ("實時", "即時"), ("教程", "教學"), ("臺", "台"),
    ("檔案照片", "文件照片"), ("圖片和檔案中", "圖片和文件中"), ("收據和檔案的照片", "收據和文件的照片"),
    ("更多資訊", "其他資訊"),                  # what Windows' own SmartScreen box says in 繁體
    # WhatsApp's own 繁體 menu: 已連結的裝置 → 連結裝置
    ("已關聯裝置", "已連結的裝置"), ("關聯新裝置", "連結裝置"), ("關聯", "連結"),
    ("安卓", "Android"), ("回車", "Enter"), ("粘回", "貼回"), ("銀行卡", "信用卡"),
    ("“", "「"), ("”", "」"), ("‘", "『"), ("’", "』"),
    # the app's interface is 简体中文 + English
    ("中英文介面", "簡體中文 / 英文介面"),
    ("中文 / 英文介面", "簡體中文 / 英文介面"),
    ("介面也有中文版", "介面也有簡體中文版"),
]


def convert(text: str) -> str:
    out = OpenCC("s2twp").convert(text)
    for a, b in FIXES:
        out = out.replace(a, b)
    out = re.sub(r"(?<!簡體)(?<!/ )中文介面", "簡體中文介面", out)
    out = re.sub(r"(?<=[一-鿿])(QR Code|Android|Enter)", r" \1", out)
    out = re.sub(r"(QR Code|Android|Enter)(?=[一-鿿])", r"\1 ", out)
    out = out.replace("](/zh/", "](/zh-hant/").replace('"/zh/', '"/zh-hant/')
    # the setup guide names the app's buttons: they are in 简体 in the app itself
    out = out.replace("## 第 1 步：", "> GlotChat 的介面目前是簡體中文和英文，下文的按鈕名稱以繁體字顯示。\n\n          ## 第 1 步：", 1)
    return "# GENERATED from zh.yaml by src/make_zh_hant.py: do not edit by hand.\n" + out


if __name__ == "__main__":
    with open(SRC, encoding="utf-8") as f:
        text = f.read()
    with open(DST, "w", encoding="utf-8", newline="\n") as f:
        f.write(convert(text))
    print("wrote", os.path.relpath(DST, os.path.dirname(HERE)))
