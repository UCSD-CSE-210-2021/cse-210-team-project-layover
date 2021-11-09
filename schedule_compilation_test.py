from LayoverMeeting import LayoverMeeting
from LayoverUser import LayoverUser

import numpy as np
import random

if __name__ == '__main__':
    meeting_id = 'asdf_id'
    name = 'dummy_name'
    meeting_type = 'remote'
    meeting_length = 2
    date_type = 'general'
    start_date = None
    end_date = None
    myMeeting = LayoverMeeting(meeting_id, name, meeting_type, meeting_length, date_type, start_date, end_date)

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

    for i in range(3):
        avail_1.append(random.choices(weights, k = 3))
        avail_2.append(random.choices(weights, k = 3))
        avail_3.append(random.choices(weights, k = 3))
        avail_4.append(random.choices(weights, k = 3))
        avail_5.append(random.choices(weights, k = 3))
    
    print('\n', avail_1, '\n')
    print('\n', avail_2, '\n')
    # print('\n', avail_3, '\n')
    # print('\n', avail_4, '\n')
    # print('\n', avail_5, '\n')


    user1.setAvailability(avail_1, avail_2)
    user2.setAvailability(avail_2, avail_2)
    user3.setAvailability(avail_3, avail_3)
    user4.setAvailability(avail_4, avail_4)
    user5.setAvailability(avail_5, avail_5)

    myMeeting.addUser(user1)
    myMeeting.addUser(user2)
    # myMeeting.addUser(user3)
    # myMeeting.addUser(user4)
    # myMeeting.addUser(user5)

    # myMeeting.compiledAvailability()
    myMeeting.bestMeetingTimes()