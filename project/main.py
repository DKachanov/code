from flask import Flask, render_template, send_file

app = Flask(__name__, template_folder="D:\\code\\project\\templates\\", static_folder="D:\\code\\project\\static\\")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/reg")
def reg():
    return render_template("reg.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")


#================
#css

@app.route("/css/index.css")
def css_index():
    return send_file("static\\css\\index.css")

@app.route("/css/login.css")
def css_login():
    return send_file("static\\css\\login.css")

@app.route("/css/profile.css")
def css_profile():
    return send_file("static\\css\\profile.css")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80)