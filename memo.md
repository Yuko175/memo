

# 対象ディレクトリを指定（現在のディレクトリにする場合は"."）
for file in *; do
    # ファイル名がディレクトリでないか確認
    if [[ -f "$file" ]]; then
        new_name="$file"

        # 全角括弧 → 半角括弧
        new_name="${new_name//（/(}"
        new_name="${new_name//）/)}"

        # 都市名のローマ字変換
        for city in "${!cities[@]}"; do
            new_name="${new_name//${city}/${cities[$city]}}"
        done

        # リネーム
        if [[ "$file" != "$new_name" ]]; then
            mv "$file" "$new_name"
            echo "Renamed: $file -> $new_name"
        fi
    fi
done
```



mkdir cnf/xxx;
cd cnf;
=CONCAT("cp template.cnf cnf/",A7,"_ ",C7,".cnf;")
sed -i -e "s/\(commonName_default\s*=\s*\).*/\1XXXXX/" "(XX) XXXXX.cnf";
sed -i -e "s/\(CN\s*=\s*\).*/\1XXXXX/" "(XX) XXXXX.cnf";
sed -i -e "s/\(DNS.1\s*=\s*\).*/\1XXXXX/" "(XX) XXXXX.cnf";
sed -i -e "s/\(IP.1\s*=\s*\).*/\1XXX.XXX.XXX.XXX/" "(XX) XXXXX.cnf";
cd ../;
openssl req -new -key server.key -out "./csr/(XX) XXXXX.csr" -config "./cnf/(XX) XXXXX.cnf";


年齢
https://j-net21.smrj.go.jp/startup/research/restaurant/cons-izakaya2.html

キャッシュレスポイント
https://pro.gnavi.co.jp/magazine/t_res/cat_3/a_4217/

推移
https://www.recruit.co.jp/newsroom/pressrelease/assets/20240925_gourmet_01.pdf

https://www.recruit.co.jp/newsroom/pressrelease/assets/20250701_gourmet_01.pdf

グラフ

https://www.meti.go.jp/statistics/toppage/report/minikaisetsu/hitokoto_kako/20250313hitokoto.html#:~:text=いるようです%E3%80%82-,外食費は増加し続けるか,てはいないようです%E3%80%82

データ

https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00200561&tstat=000000330001&cycle=0&tclass1=000001228280&tclass2val=0

NEC
https://www.necplatforms.co.jp/solution/food/mobileorder/index.html

https://jpn.nec.com/vci/optimization/index.html




A	B	C	D
1
年	内食費 (円)	中食費 (円)	外食費 (円)
2
2013	29,199	7,425	11,686
3
2014	30,064	8,024	11,595
4
2015	30,580	8,506	11,540
5
2016	30,033	8,823	11,530
6
2017	30,223	9,141	11,614
7
2018	30,022	9,436	11,833
8
2019	30,119	9,531	12,164
9
2020	32,159	9,837	9,065
10
2021	31,525	10,034	8,892
11
2022	30,958	10,483	10,256
12
2023	31,842	10,929	11,514
13
2024	32,497	11,189	12,423






https://qiita.com/iwantit/items/528423cf133013f2240f 
https://mebee.info/2021/07/22/post-29741/ https://solutions.vaio.com/5439

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


アプリのアンインストール
https://support.microsoft.com/ja-jp/windows/windows-でアプリとプログラムをアンインストールまたは削除する-4b55f974-2cc6-2d2b-d092-5905080eaf98





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

