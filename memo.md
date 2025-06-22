Urls.py

```python
urlpatterns = [
    path("", views.index, name="index"),
    path("image/", views.image, name="image"),
]
```

Views.py

```python
from django.http import HttpResponse
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from io import BytesIO
from django.shortcuts import render
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# 画面
def index(request):
    return render(request, "app/index.html")

# 画像作って返す
def image(request):

    # データ作成
    datas = [20, 30, 10]
    labels = ["Wine", "Sake", "Beer"]
    colors = ["yellow", "red", "green"]

    # グラフの前準備
    fig, ax = (
        plt.subplots()
    )  # figは、Figureオブジェクト(箱の設定)、axはAxesオブジェクト(中身の設定)
    fig.set_size_inches(2, 2)  # 画像のサイズを指定(インチ単位)
    ax.axis("equal")  # 円グラフを描画するために軸の比率を1:1に設定

    # グラフの内容
    ax.pie(
        datas,
        startangle=90,
        labels=labels,
        autopct="%1.1f%%",
        colors=colors,
        counterclock=False,
    )

    # 保存
    buffer = (
        BytesIO()
    )  # BytesIO型のインスタンスを作成(一時メモリに画像を保存するための箱を用意)
    plt.savefig(buffer, format="png")  # 画像を保存
    plt.close(fig)  # グラフを閉じる
    image_value = buffer.getvalue()  # 画像データを取得

    # 返却
    return HttpResponse(image_value, content_type="image/png")
```

index.html

```html
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>グラフ表示</title>
  </head>
  <body>
    <img src="{% url 'image' %}" alt="グラフ" />
  </body>
</html>
```
