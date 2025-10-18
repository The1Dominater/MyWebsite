from flask import Flask, render_template

app = Flask(__name__, template_folder=".")

@app.route("/")
@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/home.html")
def home():
    return render_template("home.html")

@app.route("/contact.html")
def contact():
    return render_template("contact.html")

@app.route("/portfolio.html")
def portfolio():
    return render_template("portfolio.html")

@app.route("/resume.html")
def resume():
    return render_template("resume.html")

if __name__ == "__main__":
    app.run(debug=True)
