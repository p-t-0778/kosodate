from flask import Flask, render_template, request
import pandas as pd
import json

app = Flask(__name__)

# CSV読み込み（文字コードはUTF-8 or UTF-8-SIG）
df = pd.read_csv("data/support_data.csv", encoding="utf-8-sig")

# 地域と都道府県のマッピング辞書を作成（都道府県 → 市区町村リスト）
prefecture_city_map = (
    df.groupby("都道府県")["地域"]
    .unique()
    .apply(list)
    .to_dict()
)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        city = request.form["city"]
        prefecture = request.form["prefecture"]
        income = int(request.form["income"])
        children = int(request.form["children"])
        child_age = int(request.form["child_age"])
        dual_income = request.form["dual_income"]
        disabled_child = request.form["disabled_child"]
        online_only = "online_only" in request.form

        # 絞り込み処理（AND条件）
        filtered = df[
            (df["都道府県"] == prefecture) &
            (df["地域"] == city) &
            (income <= df["年収上限"]) &
            (children >= df["子数下限"]) &
            (child_age <= df["年齢上限"])
        ]

        # 共働き条件
        filtered = filtered[
            (filtered["共働き条件"] == "不問") |
            (filtered["共働き条件"] == dual_income)
        ]

        # 障害児条件
        filtered = filtered[
            (filtered["障害児条件"] == "不問") |
            (filtered["障害児条件"] == disabled_child)
        ]

        # オンライン申請条件
        if online_only:
            filtered = filtered[filtered["オンライン申請"] == "〇"]

        results = filtered.to_dict(orient="records")

    unique_prefectures = sorted(df["都道府県"].dropna().unique())
    return render_template(
        "index.html",
        results=results,
        prefectures=unique_prefectures,
        prefecture_city_map=json.dumps(prefecture_city_map, ensure_ascii=False)
    )

if __name__ == "__main__":
    app.run(debug=True)