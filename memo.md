https://solutions.vaio.com/5439

schanel: failed to receive handshake, SSL/TLS connection failed エラーは、多くの場合、プロキシ環境下でGitが正しく設定されていないことが原因です。

Gitにプロキシ設定を行う

これが最も一般的で安全な解決策です。Gitに対して、使用しているプロキシサーバーのアドレスとポート番号を設定します。

コマンドプロンプト、PowerShell、またはGit Bashを開きます。
以下のコマンドを実行してプロキシを設定します。

<proxy-server-address> と <port> の部分を、お使いのプロキシサーバーの情報に置き換えてください。(プロキシの情報は、会社の情報システム部門などにご確認ください。)
```bush
git config --global http.proxy http://<proxy-server-address>:<port>
```
```bush
git config --global https.proxy http://<proxy-server-address>:<port>
```
プロキシで認証が必要な場合は、以下のようにユーザー名とパスワードを含めます。
```bush
git config --global http.proxy http://<username>:<password>@<proxy-server-address>:<port>
```
```bush
git config --global https.proxy http://<username>:<password>@<proxy-server-address>:<port>
```
VS Codeを完全に終了し、再起動します。
再度、VS Codeからリポジトリのクローンを試します。







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

