from layover import db
import json
import numpy as np
from itertools import groupby
from datetime import time, timedelta
from datetime import datetime

# NOTE: IF YOU CHANGE ANY PARAMETER NAME IN EACH CLASS, THAT DATABASE MUST BE RESET (AKA DELETED)

# class LayoverMeeting_SQLAlchemy(db.Model):
class Meeting(db.Model):
    '''
    meetingID
    meetingName
    meetingUsers
    meetingType
    meetingLength
    dateType
    startDate
    endDate

    TESTING
    Meeting(meetingID='aaa', meetingName='bbb', meetingType='ccc', meetingLength=15, dateType='general_week', startDate='', endDate='')
    Meeting(meetingID='111', meetingName='222', meetingType='333', meetingLength=15, dateType='general_week', startDate='', endDate='')
    '''

    # character lengths are hard coded for testing purposes!!!
    meetingID = db.Column(db.String(20), primary_key=True)
    meetingName = db.Column(db.String(20), nullable=False)
    meetingUsers = db.relationship('User', backref='author', lazy=True)
    meetingType = db.Column(db.String(20), nullable=False)
    meetingLength = db.Column(db.Integer, nullable=False)
    dateType = db.Column(db.String(20), nullable=False)
    startDate = db.Column(db.Integer, nullable=False)
    endDate = db.Column(db.Integer, nullable=False)
    dayStartTime = db.Column(db.Integer, nullable=False)
    dayEndTime = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Meeting('meetingID: {self.meetingID}', 'meetingName: {self.meetingName}')"

    def getMeetingID(self):
        return self.meetingID

    def getName(self):
        return self.meetingName

    def getUsers(self):
        return self.meetingUsers

    def getUser(self, userKey):
        try:
            return User.query.filter_by(userEmail=userKey).first()
        except KeyError:
            return None

    def getLength(self):
        return self.meetingLength

    def getMeetingType(self):
        return self.meetingType

    def getDateType(self):
        return self.dateType

    def getStartTime(self):
        return self.day_start_time

    def getEndTime(self):
        return self.day_end_time

    def addUser(self, newUser):
        self.meetingUsers.append(newUser)
        db.session.commit()

    def __eq__(self, other):
        if isinstance(other, Meeting) and other.toJSON() == self.toJSON():
            return True

        return False

    def toJSON(self):
        users = self.getUsers()
        userDict = {}
        for user in users:
            # Load back the dictionary from the dumped JSON string.
            # We want an object here and not a string
            userDict[user.getID()] = json.loads(user.toJSON())

        resultJSON = {
            "meeting_id" : self.meetingID,
            "name" : self.meetingName,
            "users" : userDict,
            "meeting_type" : self.meetingType,
            "meeting_length" : self.meetingLength,
            "date_type" : self.dateType,
            "start_date" : self.startDate,
            "end_date" : self.endDate,
            "day_start_time" : self.dayStartTime,
            "day_end_time" : self.dayEndTime
        }

        return json.dumps(resultJSON, sort_keys=True, indent=4)
		
    def compiledAvailability(self, inPerson: bool):
        users = list(self.getUsers())
        userKeys = [u.getID() for u in users]

        # Initializing template via hard coding
        # TODO: make compiled schedule dynamic, but not reliant on a key in case no availabilities added yet

        # Alex: why would you call this function though if there are no user availabilities to compile...?

        # user0 = self.getUser(userKeys[0])
        # user0_availability = np.array(user0.getInPersonAvailability())
        num_blocks_in_day = int(
            (self.dayEndTime - self.dayStartTime) * (60 / 15))

        # WARNING: FOLLOWING VALUE IS HARD CODED
        num_days = 7
        compiled_schedule = np.zeros((num_blocks_in_day, num_days))
        for userKey in userKeys:
            user = self.getUser(userKey)

            if inPerson:
                user_availability = user.getInPersonAvailability()
            else:
                user_availability = user.getVirtualAvailability()

            if user_availability is None:
                continue

            compiled_schedule += np.array(user_availability)
        if len(userKeys) > 0:
            max_val = np.max(compiled_schedule)
            if max_val > 0:
                compiled_schedule /= max_val

        # self.combined_results = compiled_schedule
        # if want list of lists,
        # comment the following line and uncomment the rest of the code
        return compiled_schedule

        # compiled_schedule_list = list()
        # for i in range(compiled_schedule.shape[0]):
        # 	compiled_schedule_list.append(compiled_schedule[i])
        # self.schedule_results = compiled_schedule_list

    def bestMeetingTimes(self, compiled_list):
        # compiled_list = self.compiledAvailability()
        # print(compiled_list)

        # start_ind = 0
        # end_ind = start_ind + self.meeting_length

        # dummy values, must change in future
        start_time = datetime(2021, 11, 4, hour=self.dayStartTime)
        # end_time = datetime(2021, 11, 4, hour=self.day_end_time)
        week_dict = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday',
                        3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}

        # key = sum of compiled availabilities over the potential meeting times, and val = (day index, time index) tuple
        best_five = {}
        for day_idx, day in enumerate(compiled_list.T):
            start_ind = 0
            end_ind = start_ind + int((self.meetingLength/15))
            while end_ind <= len(day):
                curr_sum = sum(day[start_ind:end_ind])

                if best_five:
                    # check if curr sum is greater than the current greatest
                    largest = sorted(best_five, reverse=True)[0]
                    # for i in sorted(best_five):
                    if curr_sum >= largest and curr_sum != 0:# or len(best_five) < 5 and curr_sum != 0:
                        while curr_sum in best_five:
                            curr_sum -= 0.0001
                        best_five[curr_sum] = (day_idx, start_ind)
                        new_largest = sorted(best_five, reverse=True)[0]
                        new_smallest = sorted(best_five)[0]
                        range = new_largest - new_smallest

                        # keep length to top 5
                        while range > 0.0004:
                            best_five.pop(sorted(best_five)[0])
                            new_largest = sorted(best_five, reverse=True)[0]
                            new_smallest = sorted(best_five)[0]
                            range = new_largest - new_smallest
                        # # break out of loop so we don't pop more than one
                        # break

                else:  # if dict is empty add in first value
                    if curr_sum != 0:
                        best_five[curr_sum] = (day_idx, start_ind)

                start_ind += 1
                end_ind += 1

        best_times = []
        best_times_idx = []
        for i in sorted(best_five):
            datetime_tostr = start_time+timedelta(minutes=(15*best_five[i][1]))
            best_times.insert(
                0, (week_dict[best_five[i][0]] + ' ' + datetime_tostr.strftime("%I:%M %p")))
            best_times_idx.insert(0, best_five[i])

        return best_times_idx, best_times

    # def bestMeetingTimes(self, compiled_list):
    #     # compiled_list = self.compiledAvailability()
    #     # print(compiled_list)

    #     start_ind = 0
    #     end_ind = start_ind + self.meetingLength

    #     # dummy values, must change in future
    #     start_time = datetime(2021, 11, 4, hour=7)
    #     end_time = datetime(2021, 11, 4, hour=22)
    #     week_dict = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday',
    #                  3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}

    #     # key = sum of compiled availabilities over the potential meeting times, and val = (day index, time index) tuple
    #     best_five = {}
    #     for day_idx, day in enumerate(compiled_list.T):
    #         start_ind = 0
    #         end_ind = start_ind + int((self.meetingLength/15))
    #         while end_ind <= len(day):
    #             curr_sum = sum(day[start_ind:end_ind])

    #             if best_five:
    #                 # check if curr sum is greater than any of the current top 5
    #                 for i in sorted(best_five):
    #                     if curr_sum > i or len(best_five) < 5:
    #                         while curr_sum in best_five:
    #                             curr_sum += 0.0001
    #                         best_five[curr_sum] = (day_idx, start_ind)

    #                         # if length is larger than 5, pop the smallest key
    #                         if len(best_five) > 5:
    #                             best_five.pop(sorted(best_five)[0])
    #                         # break out of loop so we don't pop more than one
    #                         break

    #             else:  # if dict is empty add in first value
    #                 best_five[curr_sum] = (day_idx, start_ind)

    #             start_ind += 1
    #             end_ind += 1

    #     best_times = []
    #     for i in sorted(best_five):
    #         datetime_tostr = start_time+timedelta(minutes=(15*best_five[i][1]))
    #         best_times.insert(
    #             0, (week_dict[best_five[i][0]] + ' ' + datetime_tostr.strftime("%H:%M")))
    #     return best_times


    # meeting length
    def bestMeetingTimesV2(self, compiled_schedule):
        # print(compiled_schedule)

        start_time = self.day_start_time
        end_time = self.day_end_time
        # 60 is hard coded b/c 60min in hour
        num_blocks_in_hour = 60 / self.meeting_length
        week_dict = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday',
                     3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
        # now each index is ordered by day; shape should be (7,64)
        transposed_schedule = compiled_schedule.T
        assert (end_time - start_time) * \
            num_blocks_in_hour == transposed_schedule.shape[1]
        indices = np.arange(0, transposed_schedule.shape[1], 1)

        scores_list = list()
        corresponding_string_list = list()
        for i in range(transposed_schedule.shape[0]):
            zipped_value_index = list(zip(indices, transposed_schedule[i]))
            # https://stackoverflow.com/questions/38277182/splitting-numpy-array-based-on-value
            nonzero_ranges_zipped = [list(g) for k, g in groupby(
                zipped_value_index, lambda x: x[1] != 0) if k]
            for zipped_range in nonzero_ranges_zipped:
                index_range, value_range = np.array(list(zip(*zipped_range)))

                # calculating score for range and time range String
                # dividing sum by length of value range because want score to be dependant on values and not length of time
                # TODO: issue with best time within a large range of values; discuss with team (calculating this score metric is a bit more complicated than Alex thought)
                score = np.sum(value_range) / len(value_range)

                #############################################################################################################
                # I think there's definitely a better way to do this... this is really disgusting
                #############################################################################################################

                # calculate the hour and minute time of the index only
                start_index = index_range[0]
                # int() automatically floors value
                start_hour = int(start_index / num_blocks_in_hour) + start_time
                start_minute = int(
                    (start_index % num_blocks_in_hour) * self.meeting_length)
                if start_minute == 0:
                    string_start_minute = '00'  # lol stupid bug...
                else:
                    string_start_minute = str(start_minute)
                start_string = str(start_hour) + ':' + string_start_minute

                # there will always be a start minute, so checking is index_range only has one value
                # NEED TO ADD {self.meeting_length} TO END MINUTE BECAUSE END TIME MUST INCLUDE LAST BLOCK OF TIME
                if len(index_range) == 1:
                    end_minute = start_minute + self.meeting_length
                    end_hour = start_hour
                    if end_minute == 60:  # need to carry over time
                        end_minute = 0
                        end_hour += 1

                    if end_minute == 0:
                        string_end_minute = '00'
                    else:
                        string_end_minute = str(end_minute)

                    end_string = str(end_hour) + ':' + string_end_minute
                    string_range = f'\"{start_string} - {end_string}\"'
                    # print(f'The range of time is {string_range}')
                else:
                    end_index = int(index_range[len(index_range)-1])
                    # int() automatically floors value
                    end_hour = int(end_index / num_blocks_in_hour) + start_time
                    end_minute = int((end_index % num_blocks_in_hour)
                                     * self.meeting_length) + self.meeting_length

                    # repeating code... gross
                    if end_minute == 60:  # need to carry over time
                        end_minute = 0
                        end_hour += 1

                    if end_minute == 0:
                        string_end_minute = '00'
                    else:
                        string_end_minute = str(end_minute)

                    # calculating end_string and displaying the range of time
                    end_string = str(end_hour) + ':' + string_end_minute
                    string_range = f'\"{start_string} - {end_string}\"'
                    # print(f'The range of time is {string_range}')

                scores_list.append(score)
                corresponding_string_list.append(string_range)

        meeting_times = list(zip(scores_list, corresponding_string_list))
        sorted_meeting_times = sorted(
            meeting_times, key=lambda x: x[0], reverse=True)
        best_time_list, corresponding_time_list = list(
            zip(*sorted_meeting_times))

        # temporary code just to show that we can output best meeting times
        n = 5
        print(f"Top {n} meeting times:")
        for i in range(n):
            print(
                f'{corresponding_string_list[i]} (Score: {best_time_list[i]})')

# class LayoverUser_SQLAlchemy(db.Model):
# BIG NOTE: ALEX CHANGED CLASS VARIABLE NAMES
class User(db.Model):
    '''
    name
    email
    meetingID
    inPersonUserAvailability
    remoteUserAvailability

    TESTING
    l1 = json.dumps(list(['dummy values']))
    l2 = json.dumps(list(['dummy values']))
    User(userName='Alex', userEmail='alex@alex.com', meetingID='aaa', inPersonUserAvailability=l1, remoteUserAvailability=l2)
    User(userName='Yen', userEmail='yen@yen.com', meetingID='aaa')
    '''

    # character lengths are hard coded for testing purposes!!!
    userName = db.Column(db.String(20), unique=False, nullable=False)
    userEmail = db.Column(db.String(50), primary_key=True)  # ERIC: is it unique based on user ID. Or is it unique based on (userID, meetingID)?
    meetingID = db.Column(db.String(20), db.ForeignKey('meeting.meetingID'), primary_key=True, nullable=False)

    # input to availability schedules should be a json.dumps() object!
    inPersonUserAvailability = db.Column(db.String(5000), unique=False) #max 5000 char...?
    remoteUserAvailability = db.Column(db.String(5000), unique=False) #max 5000 char...?

    def __repr__(self):
        return f"User('userName: {self.userName}', 'userEmail: {self.userEmail}')"

    def setAvailability(self, inPersonAvailability: list, virtualAvailability: list):
        jsonInPersonMeetingTable = json.dumps(inPersonAvailability)
        jsonVirtualMeetingTable = json.dumps(virtualAvailability)
        self.inPersonUserAvailability = jsonInPersonMeetingTable
        self.remoteUserAvailability = jsonVirtualMeetingTable

    def getName(self):
        return self.userName

    def getMeetingID(self):
        return self.meetingID

    def getID(self):
        return self.userEmail

    def getInPersonAvailability(self):
        parsedInPerson = None 
        if self.inPersonUserAvailability != None: 
            parsedInPerson = json.loads(self.inPersonUserAvailability) 
        return parsedInPerson

    def getVirtualAvailability(self):
        parsedVirtual = None 
        if self.remoteUserAvailability: 
            parsedVirtual = json.loads(self.remoteUserAvailability)
        return parsedVirtual

    def toJSON(self):
                
        resultJSON = {
            "meeting_id" : self.meetingID,
            "name" : self.userName,
            "email" : self.userEmail,
            "inPersonAvailability" : self.getInPersonAvailability(),
            "virtualAvailability" : self.getVirtualAvailability()
        }

        return json.dumps(resultJSON, sort_keys=True, indent=4)

    def __eq__(self, other):
        if isinstance(other, User) and other.toJSON() == self.toJSON():
            return True

        return False