メモ
```python
# input->物体名
# カロリー計算：料理名に対して、カロリーを計算した値が辞書型で入ってる->辞書型1

# 関数を呼び出して->物体名
# 物体名から、作れる料理名をリストで返す:料理名→素材
# その料理名のカロリーを計算して、リストで返す
# その中から、カロリーの低い順に1つ抽出
# その料理名のレシピを返す

# input-> 食べた料理
# output-> 食べた料理のカロリー(float)と、推薦料理の名前、材料、カロリー、レシピ(dict)を返す

cooking_dict = {
    "カレー": {
        "材料": ["米", "カレー粉", "肉", "野菜"],
        "カロリー": 800,
        "レシピ": "1. 米を炊く\n2. 肉と野菜を炒める\n3. カレー粉を加える",
    },
    "シチュー": {
        "材料": ["肉", "野菜", "スープ"],
        "カロリー": 600,
        "レシピ": "1. 肉と野菜を炒める\n2. スープを加える\n3. 煮込む",
    },
}


def get_calories(dish_name):
    return cooking_dict[dish_name]["カロリー"]


def find_recipes(
    available_ingredients: list, calorie: float, calorie_limit_percent: int
) -> dict:
    """
    利用可能な材料と指定したカロリー範囲内で作れるレシピを探します。

    Args:
        available_ingredients (list): 利用可能な材料のリスト。
        calorie (float): 目標とするカロリー値。
        calorie_limit_percent (int): 目標カロリーから許容するパーセント範囲。

    Returns:
        dict:
        材料とカロリー条件を満たすレシピの内、最も目標カロリーに近いものを返します。
        なお、候補が複数ある場合はすべて返します。

        また、条件に合うレシピがない場合は以下を返します。
        ```
        {
            "該当する料理がありません": {
                "材料": None,
                "カロリー": None,
                "レシピ": None
            }
        }
        ```

    Notes:
        - グローバル変数 `cooking_dict` を利用します。
        - 材料条件で絞り込み、さらにカロリーが目標値に近いものを選びます。
    """
    # 利用可能な材料から作れる料理を探す
    possible_recipe_dict = {}
    # items() を使わずキーアクセスで処理
    for key in cooking_dict:
        value = cooking_dict[key]
        include_all = True
        for item in value["材料"]:
            if item not in available_ingredients:
                include_all = False
                break
        if include_all:
            possible_recipe_dict.update({key: value})

    # カロリー制限に基づいて最適なレシピを見つける
    suggested_recipe_dict = {}
    min_diff = None
    min_calorie = calorie * (1 - calorie_limit_percent / 100)
    max_calorie = calorie * (1 + calorie_limit_percent / 100)

    for key in possible_recipe_dict:
        value = possible_recipe_dict[key]
        recipe_calorie = value["カロリー"]
        diff = abs(recipe_calorie - calorie)  # 絶対値
        if (
            min_diff is None or diff <= min_diff
        ) and min_calorie <= recipe_calorie <= max_calorie:
            min_diff = diff
            suggested_recipe_dict.update({key: value})

    if suggested_recipe_dict:
        return suggested_recipe_dict
    else:
        return {
            "該当する料理がありません": {"材料": None, "カロリー": None, "レシピ": None}
        }


def calculate_calorie(dish_name, available_ingredients, calorie, calorie_limit_percent):
    dish_calories = get_calories(dish_name)
    suggested_recipes = find_recipes(
        available_ingredients, calorie, calorie_limit_percent
    )
    return dish_calories, suggested_recipes


today_min_calories = 1700  # 今日の最低カロリー
dish_name = "シチュー"  # 昼ごはん
available_ingredients = ["米", "カレー粉", "肉", "野菜", "スープ"]  # 冷蔵庫の中身
calorie = today_min_calories - get_calories(dish_name)  # 残カロリー
calorie_limit_percent = 1000  # 許容範囲
print(
    calculate_calorie(dish_name, available_ingredients, calorie, calorie_limit_percent)
)
```
