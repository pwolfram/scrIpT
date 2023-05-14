#!/usr/bin/env python

from utilities.webformfill import submit_website_form
from datetime import datetime, timedelta


# form data for automated form submission
formurl = 'https://www.southwest.com/air/check-in/'
firstname = "Phillip"
lastname = "Wolfram"
confirmnum = "123XYZ"
flighttime = '03/14/5926 5:35 PM'

checkintime = datetime.strptime(flighttime, '%m/%d/%Y %I:%M %p') - timedelta(days=1)

while datetime.now() < checkintime:
    pass

response = submit_website_form(url= formurl,
                               formdata = dict(passengerFirstName=firstname, 
                                               passengerLastName=lastname, 
                                               confirmationNumber=confirmnum),
                                               confirmbutton='form-mixin--submit-button',
                                               retrdata='boarding-pass-container')

print(response)
