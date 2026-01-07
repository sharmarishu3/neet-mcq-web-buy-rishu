from flask import Flask, render_template, request, redirect, session
import fitz  # PyMuPDF
import os

# Flask app
app = Flask(__name__)
app.secret_key = "neetsecret"

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------- PDF MCQ EXTRACT FUNCTION --------
def extract_mcqs(pdf_path):
    doc = fitz.open(pdf_path)
    mcqs = []

    for page in doc:
        text = page.get_text("text")
        lines = [l.strip() for l in text.split("\n") if l.strip()]

        i = 0
        while i < len(lines):
            if lines[i].startswith("પ્ર.") or lines[i].startswith("Q"):
                question = lines[i]
                options = lines[i + 1:i + 5]

                answer = None
                for j in range(i + 5, min(i + 10, len(lines))):
                    if "ઉત્તર" in lines[j] or "Ans" in lines[j]:
                        answer = lines[j].split(":")[-1].strip().upper()
                        break

                if answer and len(options) == 4:
                    mcqs.append({
                        "q": question,
                        "opts": options,
                        "ans": answer
                    })

                i += 6
            else:
                i += 1

    return mcqs

# -------- ROUTES --------

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        pdf = request.files["pdf"]
        pdf_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
        pdf.save(pdf_path)

        session["mcqs"] = extract_mcqs(pdf_path)
        session["index"] = 0
        session["score"] = 0

        return redirect("/quiz")

    return render_template("upload.html")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    mcqs = session.get("mcqs", [])
    index = session.get("index", 0)

    if index >= len(mcqs):
        return f"""
        <h2>Result</h2>
        <p>Total Questions: {len(mcqs)}</p>
