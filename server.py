import string
import random

from flask import Flask
from flask import render_template, redirect
from flask import Response, request, jsonify

from LayoverCalendar import LayoverCalendar

app = Flask(__name__)

meeting_db = dict()


@app.route('/')
def home():
	return render_template('setup-landing.html')


@app.route('/handle_meeting_creation', methods=['POST'])
def handle_meeting_creation():
	# Read form results
	meeting_name = request.form['meeting_name']
	display_name = request.form['display_name']
	email = request.form['email']
	meeting_type = request.form['meeting_type']

	# Create initial calendar
	myCalendar = LayoverCalendar(meeting_name, email, display_name, meeting_type)

	# Create unique Calendar ID
	calendarID = getRandomHash()
	myKeys = meeting_db.keys()
	while calendarID in myKeys:
		calendarID = getRandomHash()

	meeting_db[calendarID] = myCalendar
	print(meeting_db)
	return "Finished"


def getRandomHash():
	available = string.ascii_letters + string.digits
	return ''.join(random.choice(available) for i in range(6))


if __name__ == "__main__":
	app.run(debug=True)
