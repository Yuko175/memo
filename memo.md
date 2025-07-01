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


将来的にはPMとして、人・技術・ビジョンをつなぎ、お客様の挑戦を支えるシステムを作りたい。
そのために3年目までに、自分の得意分野や興味の方向性を見極めたい。与えられた仕事に主体的に取り組み、小さくても「中岫さんに任せる」と言われるような成果を出すことを目指す。その中で、自分がこれを深めたい、この領域に関わりたいと思えるテーマを見つけ、専門性の軸候補を定めたい。
また、顧客やチームと関わる中で、課題解決や調整といったPMに必要な視点に触れ始めることも意識する。名前を覚えてもらえる仕事をし、「これをやりたい」と語れる準備をすることが3年目の目標にする。

将来の目標のために、
コミュニケーションスキルを身につけたい。特に、物事を(言葉の定義を確かめながら)言語化、可視化し、齟齬のない会話ができるようにすることで、異なる視点を持つ人々と共通の理解を築けるようになりたい。
3年目ではまずそのコミュニケーションスキルを意識的に実践できるようになることをゴールとする。たとえば、議論の中で不明点や曖昧な表現に対して自ら確認を入れたり、口頭の説明に図や例を加えることで相手の理解を助ける場面をつくるなど、小さな場面でスキルを使えることを目標にしたい。
また、それを支える土台として、技術や業務知識を深め、なぜその選択肢や提案が良いのかを説明できる知識を持ちたい。私は、仕事を進める上で中途半端な理解で判断したくない。だからこそ、内容を正しく理解し、それを自分の言葉で整理・伝達できる力を強みにしたい。
そうしたスキルを育てることで、お客様にとって信頼できるパートナーとなり、複雑な状況でも本質的な価値を提案できるようになりたいと考えている。



