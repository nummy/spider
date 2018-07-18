import sqlite3
from flask import Flask
from flask import jsonify
from flask import render_template

app = Flask(__name__)
conn = sqlite3.connect('python.db')
cursor = conn.cursor()


@app.route("/")
def hello():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)