#!/usr/bin/env python3
"""
Parses website to automatic fill in forms and submit.

Kicked-off / accelerated via chatGPT

Phillip Wolfram
05/14/23
"""

import mechanize
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def submit_website_form(url="https://www.southwest.com/flight/retrieveCheckinDoc.html", 
                        formdata = dict(passengerFirstName="Phillip", 
                                        passengerLastName="Wolfram", 
                                        confirmationNumber="123XYZ"),
                        confirmbutton='form-mixin--submit-button',
                        retrdata='boarding-pass-container'):
    """
        Opens up a website and sends in data.

        Phillip Wolfram
        05/14/23
    """
    # Set up the Chrome webdriver
    driver = webdriver.Safari()

    # Navigate to the website
    driver.get(url)

    # Fill out the form fields
    for aname in formdata:
        namedInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, aname))
        )
        namedInput.send_keys(formdata[aname])


    # Submit the form
    submit_button = driver.find_element_by_id(confirmbutton)
    submit_button.click()

    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, retrdata))
    )

    # Print the page source
    response = driver.page_source
    
    # Close the webdriver
    driver.quit()

    return response


def check_in(firstname, lastname, email, phonenum, confirmnum):
    """
    Legacy code requiring generalization for broader application.
    """
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