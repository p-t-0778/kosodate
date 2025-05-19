from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# CSV読み込み
df = pd.read_csv("data/support_data.csv", encoding="shift_jis")  # または UTF-8 に変更
unique_cities = sorted(df["地域"].dropna().unique())  # 地域一覧を抽出・昇順に並べる

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        city = request.form["city"]
        income = int(request.form["income"])
        children = int(request.form["children"])

        filtered = df[
            (df["地域"] == city) &
            (income <= df["年収条件"]) &
            (children >= df["子ども数条件"])
        ]
        results = filtered.to_dict(orient="records")

    return render_template("index.html", results=results, cities=unique_cities)
