from flask import Flask, render_template
import requests
import sqlite3

app = Flask(__name__)

# Create database
conn = sqlite3.connect("quotes.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT
)
""")
conn.commit()


@app.route("/")
def home():
    # Fetch random quote
    response = requests.get("https://api.quotable.io/random", verify=False)
    data = response.json()

    quote = data["content"]

    # Save quote in database
    cursor.execute("INSERT INTO quotes (quote) VALUES (?)", (quote,))
    conn.commit()

    # Get all previous quotes
    cursor.execute("SELECT quote FROM quotes")
    history = cursor.fetchall()

    return render_template("index.html", quote=quote, history=history)


if __name__ == "__main__":
    app.run(debug=True)