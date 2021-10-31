import string
import random

from flask import Flask
from flask import render_template, redirect, url_for
from flask import Response, request, jsonify

from LayoverMeeting import LayoverMeeting

app = Flask(__name__)

meeting_db = dict()


@app.route('/')
def home():
	return render_template('setup-landing.html')


@app.route('/handle_meeting_creation', methods=['POST'])
def handle_meeting_creation():
	# Read form results
	meeting_name = request.form['meeting_name']
	meeting_type = request.form['meeting_type']
	date_type = request.form['date_type']
	start_date = request.form['start_date']
	end_date = request.form['end_date']

	# Create unique Calendar ID
	meeting_id = getUniqueRandomHash()

	# Create initial meeting
	myMeeting = LayoverMeeting(meeting_id, meeting_name, meeting_type, date_type, start_date, end_date)

	meeting_db[meeting_id] = myMeeting
	print(meeting_db)
	return redirect(url_for('meeting', meeting_id=meeting_id))


def getUniqueRandomHash():
	available = string.ascii_letters + string.digits
	result = ''.join(random.choice(available) for i in range(6))
	myKeys = meeting_db.keys()
	while result in myKeys:
		result = ''.join(random.choice(available) for i in range(6))
	return result


@app.route('/meeting/<meeting_id>', methods=['GET', 'POST'])
def meeting(meeting_id):
	myMeeting = meeting_db[meeting_id]
	myData = myMeeting.toJSON()
	return render_template('scheduling-landing.html', data=myData)


@app.route('/results/<meeting_id>')
def results(meeting_id):
	myMeeting = meeting_db[meeting_id]
	return myMeeting.toJSON()


if __name__ == "__main__":
	app.run(debug=True)
