from flask import Flask,redirect,request,url_for,Response,render_template

app = Flask(__name__)

app.secret_key = "supersecret"

@app.route("/")
def home():
    return render_template("HomePage/home_page.html")

@app.route("/login")
def login():
    return render_template("Login/login.html")

@app.route("/profile")
def profile():
    return render_template("Profile/profile.html")

@app.route("/dashboard")
def dashboard():
    return render_template("Dashboard/dashboard.html")

@app.route("/crop_prediction")
def crop_prediction():
    return render_template("Crop_Prediction/crop_prediction.html")

@app.route("/farmer_community")
def farmer_community():
    return render_template("Farmer_Community/farmer_community.html")