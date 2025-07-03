ロボットアイコン
https://www.irasutoya.com/2014/11/blog-post_288.html?m=1

フリーイラスト
https://soco-st.com

写真
https://unsplash.com/ja

あなたの投稿
ID
タイトル
内容
日時
Eメール
ウェルビーのしゅるい
いいねリレ
いいね数
ジャンルリレ
ジャンル画像
投稿リレ
コメント

ジャンル
ウェルビーしゅるい
ウェルビー内容
ウェルビー画像
あなたの投稿リレ
カウント

コメント
ID
Eメール
日時
本文
ユーザリレ
ユーザ名
画像

いいね
ID

投稿一覧
ろうID
タイトル
ウェルビー種類
内容
日時
Eメール
ユーザリレ
ユーザ名
ジャンルリレ
ジャンル画像
コメントリレ
いいねリレ
いいね数







オーバーロード
logging

```Python
import pandas as pd
from functools import singledispatch
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s : %(message)s"
)


def main():
    dataFrame = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
    converted_dict = convert(dataFrame)
    df = pd.DataFrame(converted_dict)


@singledispatch
def convert(arg):
    logger.debug("default convert called")
    logger.info(f"Converting {type(arg)}")
    return arg


@convert.register(pd.DataFrame)
def _(arg):
    logger.warning("convert called with pd.DataFrame")
    dict = arg.to_dict(orient="records")
    return convert(dict)

def handle_convert(arg):
    match arg:
        case pd.DataFrame():
            return convert(arg.to_dict(orient="records"))
        case _:
            return convert(arg)


if __name__ == "__main__":
    main()
```

