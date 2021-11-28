import string
import random
import json

from flask import render_template, redirect, url_for
from flask import Response, request
from layover import app, db
from layover.models import User, Meeting

@app.route('/')
def home():
    return render_template('setup-landing.html')


@app.route('/handle_meeting_creation', methods=['POST'])
def handle_meeting_creation():
    # Read form results
    requestedMeetingName = request.form['meeting_name']
    requestedMeetingType = request.form['meeting_type']
    requestedMeetingLength = int(request.form['meeting_length'])
    # date_type = request.form['date_type']  			# Uncomment for milestone 2
    # start_date = request.form['start_date']  		# Uncomment for milestone 2
    # end_date = request.form['end_date']  			# Uncomment for milestone 2
    day_start_time = int(request.form['start_time'])
    day_end_time = int(request.form['end_time'])

    requestedDateType = 'general_week'  					# Remove for milestone 2
    requestedStartDate = ''  								# Remove for milestone 2
    requestedEndDate = ''  									# Remove for milestone 2

    # Create unique Calendar ID
    generatedMeetingID = getUniqueRandomHash()

    # Create initial meeting
    # myMeeting = LayoverMeeting(
    #     meeting_id, meeting_name, meeting_type, meeting_length, date_type, start_date, end_date)

    '''meetingID
    meetingName
    meetingUsers
    meetingType
    meetingLength
    dateType
    startDate
    endDate'''

    myMeeting = Meeting(meetingID=generatedMeetingID, meetingName=requestedMeetingName, meetingType=requestedMeetingType,
        meetingLength=requestedMeetingLength, dateType=requestedDateType, startDate=requestedStartDate, endDate=requestedEndDate,
        dayStartTime=day_start_time, dayEndTime=day_end_time)
		
    db.session.add(myMeeting)
    db.session.commit()
    # meeting_db[meeting_id] = myMeeting

    return redirect(url_for('meeting', meeting_id=generatedMeetingID))


@app.route('/submitAvailability', methods=['POST', 'GET'])
def submitAvailability():

    '''
    TESTING
    User(meetingID='Alex', name='bbb', meetingType='ccc', meetingLength=15, dateType='general_week', startDate='', endDate='')
    '''

    data = request.get_json()
    print(data)
    inPersonMeetingTable = json.dumps(data['inPersonMeetingTable'])
    virtualMeetingTable = json.dumps(data['virtualMeetingTable'])
    meeting_id = data['meeting_id']
    user_email = data['email']
    # user_name = data['user_name']

    # layoverUser = User(name=user_name, email=user_email, meetingID=meeting_id, inPersonUserAvailability=inPersonMeetingTable, remoteUserAvailability=virtualMeetingTable)

    # setAvailability() from LayoverUser is now here
    currUser = User.query.filter_by(meetingID=meeting_id, userEmail=user_email).first()
    currUser.inPersonUserAvailability = inPersonMeetingTable
    currUser.remoteUserAvailability = virtualMeetingTable
    db.session.add(currUser)
    db.session.commit()

    return Response("Success", status=200)


def getUniqueRandomHash():
    available = string.ascii_letters + string.digits
    result = ''.join(random.choice(available) for _ in range(6))
    myKeys = list([query.meetingID for query in Meeting.query.all()]) # gets list of all meetingIDs
    while result in myKeys:
        result = ''.join(random.choice(available) for _ in range(6))
    return result


@app.route('/meeting/<meeting_id>', methods=['GET', 'POST'])
def meeting(meeting_id):
    myMeeting = Meeting.query.filter_by(meetingID=meeting_id).first()
    print("reached")
    print(myMeeting)
    print(type(myMeeting))
    # myMeeting = meeting_db[meeting_id]
    myData = myMeeting.toJSON()
    print("myData is: " , myData)
    return render_template('scheduling-landing.html', data=myData)

@app.route('/handle_user_info', methods=['POST'])
def handle_user_info():
    user_name = request.form['display_name']
    email = request.form['email']
    meeting_id = request.form['meeting_id']
    print("meeting id is: " , meeting_id)
    myMeeting = Meeting.query.filter_by(meetingID=meeting_id).first()
    print("myMeeting is: ", myMeeting)
    usernames = [u.getID() for u in myMeeting.getUsers()]
    print("usernames", usernames)
    # addUser() from LayoverMeeting is now here
    if email not in usernames:
        layoverUser = User(userName=user_name, userEmail=email, meetingID=meeting_id)
        db.session.add(layoverUser)
        db.session.commit()
    return redirect(url_for('availability', meeting_id=meeting_id, email=email))


@app.route('/availability/<meeting_id>/<email>')
def availability(meeting_id, email):
    # this is getting the user for the specific meetingID
    myUser = User.query.filter_by(meetingID=meeting_id, userEmail=email).first()
    meeting = Meeting.query.filter_by(meetingID=meeting_id).first()
    # someData = myUser.toJSON()
    # print("someData is: " , someData)
    return render_template('scheduling-availability.html', data=myUser.toJSON(), meeting=meeting.toJSON())
    # return render_template('scheduling-availability.html', data=myUser.toJSON(), data2=meetingType)


@app.route('/results/<meeting_id>')
def results(meeting_id):
    # Meeting Information
    myMeeting = Meeting.query.filter_by(meetingID=meeting_id).first()
    meeting_json = myMeeting.toJSON()

    # compile in-person availability
    combined_results_inperson = myMeeting.compiledAvailability(
        True)
    lists = combined_results_inperson.tolist()
    compiled_inperson = json.dumps(lists)

    # Top 5 best timings for in-person
    schedule_results = myMeeting.bestMeetingTimes(
        combined_results_inperson)
    best_times_inperson = json.dumps(schedule_results)

    # compile virtual availability
    combined_results_virtual = myMeeting.compiledAvailability(
        False)
    lists = combined_results_virtual.tolist()
    compiled_virtual = json.dumps(lists)

    # Top 5 best timings for virtual
    schedule_results = myMeeting.bestMeetingTimes(
        combined_results_virtual)
    best_times_virtual = json.dumps(schedule_results)

    data = '{"meeting_info":' + meeting_json + ',"compiled_inperson":' + compiled_inperson + ',"best_times_inperson":' \
        + best_times_inperson + ',"compiled_virtual":' + compiled_virtual + \
        ',"best_times_virtual":' + best_times_virtual + '}'
    return render_template('results.html', data=data)