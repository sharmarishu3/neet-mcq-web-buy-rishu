from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "neetsecret"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        session["score"] = 0
        session["total"] = 5
        return redirect("/quiz")
    return render_template("upload.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        if request.form.get("ans") == "a":
            session["score"] += 1

        session["total"] -= 1
        if session["total"] <= 0:
            return redirect("/result")

    return """
    <h2>Sample Question</h2>
    <form method="post">
        <input type="radio" name="ans" value="a"> Option A<br>
        <input type="radio" name="ans" value="b"> Option B<br><br>
        <button type="submit">Next</button>
    </form>
    """

@app.route("/result")
def result():
    return f"""
    <h2>Result</h2>
    <p>Score: {session.get('score', 0)}</p>
    """

if __name__ == "__main__":
    app.run(debug=True)

