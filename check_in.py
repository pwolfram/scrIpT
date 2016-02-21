#!/usr/bin/env python

import mechanize
from datetime import datetime, timedelta

def check_in(firstname, lastname, email, phonenum, confirmnum):
    br = mechanize.Browser()

    br.open("https://www.southwest.com/flight/retrieveCheckinDoc.html")

    br.select_form(name='retrieveItinerary')
    br["confirmationNumber"] = confirmnum
    br["firstName"] = firstname
    br["lastName"] = lastname

    response1 = br.submit()
    
    br.select_form(name='checkinOptions')
    response2 = br.submit(name='printDocuments', label='Check In')

    br.select_form(nr=1)

    # email option
    #br.form.set_value(['optionEmail'],name='selectedOption')
    #br["emailAddress"] = email
    
    # text option
    br.form.set_value(['optionText'],name='selectedOption')
    num = phonenum.split('-')
    br["phoneArea"] = num[0]
    br["phonePrefix"] = num[1]
    br["phoneNumber"] = num[2]
    
    response3 = br.submit(name='book_now')

    return response3

# form data
firstname = "Phillip"
lastname = "Wolfram"
confirmnum = "XYZ123"
flighttime = '01/01/2016 3:00PM'
email = "phillipwolfram@gmail.com"
phonenum = "123-456-7890"

checkintime = datetime.strptime(flighttime, '%m/%d/%Y %I:%M%p') - timedelta(days=1) + timedelta(seconds=5)

while datetime.now() < checkintime:
    pass

response = check_in(firstname, lastname, email, phonenum, confirmnum)

print response.read()
