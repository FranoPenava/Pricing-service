import os
from flask import Flask, render_template, request
from blueprints.alerts import alert
from blueprints.stores import store_blueprint
from blueprints.users import user_blueprint
from libs.mailgun import Mailgun
from dotenv import load_dotenv

app = Flask(__name__)

app.secret_key = "1234"
app.config.update(
    ADMIN=os.environ.get("ADMIN")
)

@app.route("/")
def home():
    return render_template("home.html")

app.register_blueprint(alert)
app.register_blueprint(store_blueprint)
app.register_blueprint(user_blueprint)

if __name__ == "__main__":
    app.run(debug=True)

