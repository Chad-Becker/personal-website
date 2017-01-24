from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SubmitField, validators, HiddenField
from wtforms.validators import Required, Length
from flask_mysqldb import MySQL
import datetime
import os

application = Flask(__name__)

application.config.from_pyfile("configuration.py")

db = MySQL(application)

clientUTCOffset = 0

class visitorsForm(FlaskForm):
	firstName = TextField(validators = [Required("Enter your first name"), Length(max = 20, message = "Too many characters")])
	lastName = TextField(validators = [Required("Enter your last name"), Length(max = 20, message = "Too many characters")])
	city = TextField("City", validators = [Required("Enter your city"), Length(max = 30, message = "Too many characters")])
	stateCountry = TextField("State or Country", validators = [Required("Enter your state or country"), Length(max = 30, message = "Too many characters")])
	comments = TextAreaField("Comments", validators = [Required("Please enter a comment"), Length(max = 2000, message = "Too many characters")])

@application.route("/")
def index():
	conn = db.connection
	cur = conn.cursor()
	cur.execute('''UPDATE siteHits SET lastHit=%s WHERE id=1;''', (datetime.datetime.utcnow(),))
	conn.commit()
	cur.close()
	return render_template("index.html", form = visitorsForm(), reloadPage = 0)

@application.route('/clientTimeOffset', methods = ["POST"])
def clientTimeOffset():
	shift = request.form.get('clientOffset')
	setClientOffset(shift)
	return jsonify(result = shift)

def setClientOffset(shift):
	global clientUTCOffset
	clientUTCOffset = shift

def getClientOffset():
	return clientUTCOffset

@application.route("/visitorSubmit", methods = ["POST"])
def visitorSubmit():
	if request.method == "POST":
		form = visitorsForm(request.form)

		if form.validate():
			conn = db.connection
			cur = conn.cursor()
			cur.execute('''INSERT INTO visitorsLog (firstName, lastName, city, stateCountry, visitorLocalOffset, utcTime,
				comments, reviewed, cleaning) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);''', (request.form["firstName"],
					request.form["lastName"], request.form["city"], request.form["stateCountry"], getClientOffset(),
					datetime.datetime.utcnow(), request.form["comments"], 0, 0))
			conn.commit()
			flash("")
			cur.close()

		else:
			return render_template("index.html", form = form, reloadPage = 1)
			
	return redirect(url_for("index", _anchor = "visitorsLog"))

if __name__ == "__main__":
	application.run(threaded=True)
