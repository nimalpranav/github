# app.py
from flask import Flask, request, redirect, render_template_string
import uuid

app = Flask(__name__)
storage = {}  # In-memory storage

TEMPLATE = """
<!doctype html>
<title>Code Publisher</title>
<h2>Online Code Publisher</h2>
<form method="post">
  <textarea name="code" rows="20" cols="80">{{ code or '' }}</textarea><br>
  <button type="submit">Publish</button>
</form>
{% if link %}
  <p>Shareable Link: <a href="{{ link }}">{{ link }}</a></p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        code = request.form["code"]
        code_id = str(uuid.uuid4())[:8]
        storage[code_id] = code
        link = request.url_root + "code/" + code_id
        return render_template_string(TEMPLATE, code=code, link=link)
    return render_template_string(TEMPLATE, code='', link=None)

@app.route("/code/<code_id>")
def view_code(code_id):
    code = storage.get(code_id, "Code not found.")
    return f"<pre>{code}</pre>"

if __name__ == "__main__":
    app.run(debug=True)
