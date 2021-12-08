from LayoverMeeting import LayoverMeeting
from LayoverUser import LayoverUser
import json

import numpy as np
import random

def convertNumpyMatrixToListOfLists(numpyMatrix):
        compiledScheduleList = list()
        for i in range(numpyMatrix.shape[0]):
        	compiledScheduleList.append(numpyMatrix[i])
        return compiledScheduleList

if __name__ == '__main__':
    meeting_id = 'asdf_id'
    name = 'dummy_name'
    meeting_type = 'remote'
    meeting_length = 15
    date_type = 'general'
    start_date = None
    end_date = None
    myMeeting = LayoverMeeting(meeting_id, name, meeting_type, meeting_length, date_type, start_date, end_date)

    day_start_time = myMeeting.day_start_time
    day_end_time = myMeeting.day_end_time

    name_1 = 'Alex'
    email_1 = 'alex@alex.com'

    name_2 = 'Sasya'
    email_2 = 'sasya@sasya.com'
    
    name_3 = 'Eric'
    email_3 = 'eric@eric.com'

    name_4 = 'Sunwoo'
    email_4 = 'sunwoo@sunwoo.com'

    name_5 = 'Anya'
    email_5 = 'anya@anya.com'

    user1 = LayoverUser(name_1, email_1, meeting_id)
    user2 = LayoverUser(name_2, email_2, meeting_id)
    user3 = LayoverUser(name_3, email_3, meeting_id)
    user4 = LayoverUser(name_4, email_4, meeting_id)
    user5 = LayoverUser(name_5, email_5, meeting_id)

    avail_1 = list()
    avail_2 = list()
    avail_3 = list()
    avail_4 = list()
    avail_5 = list()

    weights = list([0, 0.75, 1])

    num_days = 7
    num_blocks_in_day = int((day_end_time - day_start_time) * (60 / myMeeting.meeting_length))

    for i in range(num_blocks_in_day):
        avail_1.append(random.choices(weights, k = num_days))
        avail_2.append(random.choices(weights, k = num_days))
        avail_3.append(random.choices(weights, k = num_days))
        avail_4.append(random.choices(weights, k = num_days))
        avail_5.append(random.choices(weights, k = num_days))
    
    # print('\n', avail_1, '\n')
    # print('\n', avail_2, '\n')
    # print('\n', avail_3, '\n')
    # print('\n', avail_4, '\n')
    # print('\n', avail_5, '\n')

    user1.setAvailability(inPersonAvailability=avail_1, virtualAvailability=avail_1)
    user2.setAvailability(inPersonAvailability=avail_2, virtualAvailability=avail_2)
    user3.setAvailability(inPersonAvailability=avail_3, virtualAvailability=avail_3)
    user4.setAvailability(inPersonAvailability=avail_4, virtualAvailability=avail_4)
    user5.setAvailability(inPersonAvailability=avail_5, virtualAvailability=avail_5)

    myMeeting.addUser(user1)
    myMeeting.addUser(user2)
    myMeeting.addUser(user3)
    myMeeting.addUser(user4)
    myMeeting.addUser(user5)

    '''
    TODO: TEST CONVERTING LIST OF LISTS TO JSON AND THEN BACK
    '''
    print()
    user1AvailTest = user1.getInPersonAvailability()
    # print(user1AvailTest)
    json_avail = json.dumps(user1AvailTest)
    print(len(json_avail))
    json_avail_load = json.loads(json_avail)
    print(json_avail_load[0][0])

    compiled_schedule = myMeeting.compiledAvailability(True)

    best_times = myMeeting.bestMeetingTimes(compiled_schedule)
    print(best_times)

    '''
    # print(compiled_schedule)
    # print()
    # the following code is purely for testing - Alex
    transposed_schedule = compiled_schedule.T
    num_zeros = transposed_schedule.shape[1] - transposed_schedule.shape[0]
    # print(transposed_schedule.shape)
    for i in range(transposed_schedule.shape[0]):
        zeros = np.zeros((num_zeros))
        transposed_schedule[i][i:num_zeros+i] = zeros
    # new_compiled_schedule = transposed_schedule.T
    # myMeeting.bestMeetingTimesV2(new_compiled_schedule)
    '''