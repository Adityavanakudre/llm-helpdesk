from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/user-dashboard")
def user_dashboard():
    return render_template("user_dashboard.html")

# (optional) IT dashboard for later
@app.route("/it-dashboard")
def it_dashboard():
    return render_template("it_dashboard.html")

if __name__ == "__main__":
    app.run(port=8000, debug=True)
