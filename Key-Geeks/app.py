from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Dummy user credentials (Replace with database logic later)
users = {"user1": "password123", "trooper1": "securepass"}

# Chatbot Responses (Moved to Python for easier management)
chatbot_responses = {
    "i want to go to a particular place daily market at (\\d+:\\d+ (am|pm)). is it safe?": "The crime rate in the area is 58%, which falls under the orange category. This means you can move, but caution is advised.",
    "suggest the safest route to reach daily market": "The safest route is: Sarana → Plant Site → Ispat → Sail Chowk → Railway Station Road → Daily Market.",
    "is the area safe to walk at night": "Yes, the area is generally safe to walk at night.",
    "does elvyra provide a transport system": "Yes, Elvyra provides a transport system.",
    "what is the safest time to travel to my destination": "The safest time to travel to your destination is 1:17 PM.",
    "hii": "Hello! how can I assist you today?",
    "Hi": "Hey how can I assist you today?",
    "hey": "Hello! how can I assist you today?",
    "hello": "Hello! how can I assist you today?",
    "Shree Radhe Radhe": "Shree Radhe Radhe! How Can I Assist You Today?",
    "Hare Krishna": "Shree Radhe Krishna",
    "what should i do if i feel unsafe": """If you feel unsafe:
                            Contact your family members.
                            Trigger SOS.
                            Contact local police administration or reach the nearest police station.
                            Call central police at 100.""",
    "where is the nearest police station": "The nearest police station is Udit Nagar Police Station (via Mahtab Road)."
}

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

@app.route("/get_chatbot_response")
def get_chatbot_response():
    user_message = request.args.get("msg", "").lower()
    response = "I am sorry, I don't have the answer to that question."  # Default
    for question, answer in chatbot_responses.items():
        import re
        regex = re.compile(question, re.IGNORECASE) #Case-insensitive
        if regex.search(user_message):
            response = answer
            break
    return jsonify(response=response) # Return the response as JSON

if __name__ == "__main__":
    app.run(debug=True)
