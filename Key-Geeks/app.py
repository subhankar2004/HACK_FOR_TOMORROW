from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy user credentials (Replace with database logic later)
users = {"user1": "password123", "trooper1": "securepass"}

@app.route("/")
def loading():
    return render_template("loading.html")  # Start with loading page

@app.route("/index")
def home():
    return render_template("index.html")  # Redirects to the main page

@app.route("/user_login", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        elv_id = request.form.get("elv_id")
        password = request.form.get("password")
        if users.get(elv_id) == password:
            return redirect(url_for("user_dashboard"))
        else:
            return "Invalid Credentials. Try again!"
    return render_template("user_login.html")

@app.route("/user_dashboard", methods=["GET", "POST"])
def user_dashboard():
    if request.method == "POST":
        return redirect(url_for("transport_system"))
    return render_template("user_dashboard.html")

@app.route("/transport_system", methods=["GET", "POST"])
def transport_system():
    if request.method == "POST":
        return redirect(url_for("map_interface"))
    return render_template("transport_system.html")

@app.route("/map_interface", methods=["GET", "POST"])
def map_interface():
    if request.method == "POST":
        selected_bus = request.form.get("bus")
        if selected_bus:
            return redirect(url_for("show_map", bus=selected_bus))
        else:
            return "No bus selected", 400  # Bad request if no bus is selected
    return render_template("map_interface.html")

@app.route("/show_map")
def show_map():
    bus = request.args.get("bus", "Unknown Bus")
    return f"Showing map for bus: {bus}"

@app.route("/trooper_login", methods=["GET", "POST"])
def trooper_login():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("password")
        if users.get(user_id) == password:
            return redirect(url_for("trooper_dashboard"))
        else:
            return "Invalid Credentials. Try again!"
    return render_template("trooper_login.html")

@app.route("/trooper_dashboard")
def trooper_dashboard():
    return render_template("trooper_dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
