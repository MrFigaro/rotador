from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"espera": [], "ya_jugaron": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    data = load_data()
    if request.method == "POST":
        nick = request.form.get("nick")
        if nick and nick not in data["espera"] and nick not in data["ya_jugaron"]:
            data["espera"].append(nick)
            save_data(data)
        return redirect(url_for("index"))
    return render_template("index.html")

@app.route("/admin")
def admin():
    data = load_data()
    espera = data["espera"]
    ya_jugaron = data["ya_jugaron"]
    siguiente = espera[:9]
    return render_template("admin.html", espera=espera, ya_jugaron=ya_jugaron, siguiente=siguiente)

@app.route("/marcar/<nick>")
def marcar(nick):
    data = load_data()
    if nick in data["espera"]:
        data["espera"].remove(nick)
        data["ya_jugaron"].append(nick)
        save_data(data)
    return redirect(url_for("admin"))

@app.route("/reiniciar")
def reiniciar():
    save_data({"espera": [], "ya_jugaron": []})
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(debug=True)