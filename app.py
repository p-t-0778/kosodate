from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# CSV読み込み
df = pd.read_csv("data/support_data.csv", encoding="utf-8-sig")
unique_cities = sorted(df["地域"].dropna().unique())  # 地域一覧を抽出・昇順に並べる

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

        # 基本フィルター（市区町村・年収・子ども数・年齢）
        filtered = df[
            (df["都道府県"] == prefecture) &
            (df["地域"] == city) &
            (income <= df["年収上限"]) &
            (children >= df["子数下限"]) &
            (child_age <= df["年齢上限"])
        ]

        # 共働き条件
        filtered = filtered[
            (df["共働き条件"] == "不問") | (df["共働き条件"] == dual_income)
        ]

        # 障害児条件
        filtered = filtered[
            (df["障害児条件"] == "不問") | (df["障害児条件"] == disabled_child)
        ]

        # オンライン申請フィルタ
        if online_only:
            filtered = filtered[filtered["オンライン申請"] == "〇"]

        results = filtered.to_dict(orient="records")

    unique_cities = sorted(df["地域"].dropna().unique())
    return render_template("index.html", results=results, cities=unique_cities)

