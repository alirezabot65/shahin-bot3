from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db, get_bot, save_bot
import requests

app = Flask(__name__)
app.secret_key = "change-this-secret-key-later"

init_db()

class RubikaBotAPI:
    def __init__(self, token):
        self.token = token
        self.base = f"https://botapi.rubika.ir/v3/{token}"

    def get_me(self):
        try:
            r = requests.post(f"{self.base}/getMe", timeout=10)
            return r.json()
        except:
            return {"ok": False}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        token = request.form.get("token","").strip()
        if not token:
            flash("توکن را وارد کنید.")
            return redirect(url_for("login"))

        api = RubikaBotAPI(token)
        info = api.get_me()
        if not info.get("ok") and not info.get("data"):
            flash("توکن معتبر نیست یا اتصال برقرار نشد.")
            return redirect(url_for("login"))

        bot = info.get("data", {}) or info.get("bot", {})
        save_bot(token, bot)
        session["token"] = token
        return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    token = session.get("token")
    if not token:
        return redirect(url_for("login"))
    bot = get_bot(token)
    return render_template("dashboard.html", bot=bot)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
