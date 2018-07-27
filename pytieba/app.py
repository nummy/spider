import sqlite3
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/topic")
def get_topic():
    conn = sqlite3.connect('python.db')
    cursor = conn.cursor()
    # total = 0
    # sql = "select count(*) from topic"
    # c = cursor.execute(sql)
    # total = c.fetchone()[0]
    # total = int(total)
    sql = "select * from topic"
    c = cursor.execute(sql)
    rows = c.fetchall()
    conn.close()
    data_lst = []
    for row in rows:
        data = {
            "id": row[0],
            "title": row[1],
            "url": row[2],
            "author": row[3],
            "publish_time": row[4],
            "response_num": row[5],
            "last_reply": row[6],
            "keyword": row[7],
            "create_time": row[8],
            "update_time": row[9]
        }
        print(data)
        data_lst.append(data)
    return jsonify(data_lst)

@app.route("/clear")
def clear_all():
    conn = sqlite3.connect('python.db')
    cursor = conn.cursor()
    sql = "delete from topic"
    c = cursor.execute(sql)
    conn.commit()
    conn.close()
    return jsonify({})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)