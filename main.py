from flask import Flask, request
from report import generate_report

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def default_route():
    url = request.args.get("url")
    if url:
        return generate_report(url)

    with open("templates/home.html", "r", encoding = "utf-8") as f:
        return f.read()


if __name__ == "__main__":
    app.run(debug = True)
