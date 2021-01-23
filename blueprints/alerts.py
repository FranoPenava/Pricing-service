import json
from flask import Blueprint, render_template, request, redirect, url_for, session
from models.alert import Alert
from models.item import Item
from models.user import User
from models.store import Store
from models.decorators import requires_login

alert = Blueprint("alert", __name__)

@alert.route("/alert")
@requires_login
def index():
    alerts = Alert.find_many_by("user_email", session["email"])
    return render_template("alert_index.html", alerts = alerts)

@alert.route("/new_alert", methods = ["GET", "POST"])
@requires_login
def new_alert():
    if request.method == "POST":
        alert_name = request.form["name"]
        item_url = request.form["item_url"]
        price_limit = float(request.form["price_limit"])

        store = Store.find_by_url(item_url)
        query = json.loads(store.query)
        item = Item(item_url, store.tag_name, query)
        item.load_price()
        item.save_to_mongo()

        Alert(alert_name, item._id, session["email"], price_limit).save_to_mongo()
    
    return render_template("new_alert.html")

@alert.route("/edit/<string:alert_id>", methods=["GET", "POST"])
@requires_login
def edit_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    
    if request.method == "POST":
        price_limit = float(request.form["price_limit"])
        name = request.form["name"]

        alert.price_limit = price_limit
        alert.name = name
        alert.save_to_mongo()

        return redirect(url_for("alert.index"))
    
    return render_template("edit_alert.html", alert=alert)

@alert.route("/del/<string:alert_id>")
@requires_login
def delete_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    if alert.user_email == session["email"]:
        alert.remove_from_mongo()
    
    return redirect(url_for("alert.index"))
