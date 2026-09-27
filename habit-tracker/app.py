from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date, timedelta

app = Flask(__name__)
DB_PATH = "habits.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            streak INTEGER DEFAULT 0,
            last_completed TEXT
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()
    habits = conn.execute("SELECT * FROM habits ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", habits=habits, today=str(date.today()))


@app.route("/add", methods=["POST"])
def add_habit():
    name = request.form.get("name", "").strip()
    if name:
        conn = get_db()
        conn.execute(
            "INSERT INTO habits (name, streak, last_completed) VALUES (?, 0, NULL)",
            (name,),
        )
        conn.commit()
        conn.close()
    return redirect(url_for("index"))


@app.route("/complete/<int:habit_id>", methods=["POST"])
def complete_habit(habit_id):
    conn = get_db()
    habit = conn.execute("SELECT * FROM habits WHERE id = ?", (habit_id,)).fetchone()
    today = date.today()

    if habit:
        last = habit["last_completed"]
        yesterday = str(today - timedelta(days=1))

        if last == str(today):
            pass  # already marked today - don't double count
        elif last == yesterday:
            conn.execute(
                "UPDATE habits SET streak = streak + 1, last_completed = ? WHERE id = ?",
                (str(today), habit_id),
            )
        else:
            conn.execute(
                "UPDATE habits SET streak = 1, last_completed = ? WHERE id = ?",
                (str(today), habit_id),
            )
        conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:habit_id>", methods=["POST"])
def delete_habit(habit_id):
    conn = get_db()
    conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
