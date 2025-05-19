from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# CSVの読み込み
df = pd.read_csv("data/support_data.csv")

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        city = request.form["city"]
        income = int(request.form["income"])
        children = int(request.form["children"])

        # 条件に合う行だけ抽出
        filtered = df[
            (df["地域"] == city) &
            (income <= df["年収条件"]) &
            (children >= df["子ども数条件"])
        ]
        results = filtered.to_dict(orient="records")

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
