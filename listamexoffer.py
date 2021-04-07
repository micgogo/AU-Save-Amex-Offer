import re
import sys
import time
import datetime
import xlsxwriter
from datetime import timedelta, date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


position = 0
switch = 0
All_Offers = {}
#Text file contain all amex login details
filelocation = "C:/WebDriver/test.txt"
#Location to the firefox web driver
firefoxdriver = "C:/WebDriver/x64/geckodriver.exe"

def is_element_exist(driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@data-view-name='ENROLLED']")))
    except TimeoutException:
        return False
    return True

def nextCard(driver):
    global position
    global switch

    #Click card selection section
    try:
        element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'btn-sm btn-secondary border-dark dls-black')]")))
    finally:
        element.click()
    
    time.sleep(6)

    #Click View All in card selection if exists
    if (driver.find_elements_by_xpath("//a[@title='View All']")):
        driver.find_element_by_xpath("//a[@title='View All']").click()

    #Count how many cards
    try:
        element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[@class='collapsible-header margin-1-l-sm-down margin-2-l-md-up']")))
    finally:
        allcards = driver.find_elements_by_xpath("//*[@class='collapsible-header margin-1-l-sm-down margin-2-l-md-up']")

    #Click on the next card
    if (position < (len(allcards) - 1)):
        allcards[position].click()
        position = position + 1
    else:
        allcards[position].click()
        switch = 1
    time.sleep(10)

def movetoposition(driver, positionelement):
    desired_y = (positionelement.size['height'] / 2) + positionelement.location['y']
    current_y = (driver.execute_script('return window.innerHeight') / 2) + driver.execute_script('return window.pageYOffset')
    scroll_y_by = desired_y - current_y + 150
    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)


def getoffer(driver):
    global All_Offers

    if(driver.find_elements_by_xpath("//a[@class='btn btn-block margin-auto margin-0-tb']")):
        element = driver.find_element_by_xpath("//a[@class='btn btn-block margin-auto margin-0-tb']")
        movetoposition(driver, element)
        element.click()
        time.sleep(10)

    Offer_details = driver.find_elements_by_xpath("//p[@class='heading-3 margin-0-b dls-accent-gray-06']")
    Offer_Brand = driver.find_elements_by_xpath("//p[@class='body-1 margin-0-b dls-accent-gray-05']")
    Offer_Card = driver.find_elements_by_xpath("//div[@class='col-sm-12 col-md-3 pad-0-l']")
    Offer_End = driver.find_elements_by_xpath("//div[@class='offer-expires offer-column margin-auto-l margin-b-md-down col-md-2']")

    i = 0
    while (i < len(Offer_details)):
        CardNo = Offer_Card[i].text.split("Saved to Card -")[1]
        EndDate = Offer_End[i].text
        if (EndDate.find("\n")):
            EndDate = EndDate.replace("EXPIRES\n", "")

        if (EndDate.find("in") != -1):
            EndDate = EndDate[EndDate.find("in")+2:EndDate.find("days")].strip()
            today = date.today()
            ExpireDate = date.today() + datetime.timedelta(days=int(EndDate))
            if (len(str(ExpireDate.month)) != 2):
                emonth = "0" + str(ExpireDate.month)
            else:
                emonth = str(ExpireDate.month)
            NewExpireDate = str(ExpireDate.day) + "/" + emonth + "/" + str(ExpireDate.year)
        else:
            NewExpireDate = EndDate

        All_Offers.setdefault(CardNo, []).append(Offer_Brand[i].text)
        All_Offers.setdefault(CardNo, []).append(Offer_details[i].text)
        All_Offers.setdefault(CardNo, []).append(NewExpireDate)
        i = i + 1

    



def listamexoffer(loginname, loginpassword):
    global position
    global switch
    global All_Offers

    #Path to the selenium firefox WebDriver executable
    driver = webdriver.Firefox(executable_path=firefoxdriver)
    #Amex AU login page
    driver.get("https://www.americanexpress.com/en-au/account/login?inav=iNavLnkLog")
    
    #Wait for login username field to load put in username
    try:
        element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "eliloUserID")))
    finally:
        element.send_keys(loginname)

    #Wait for login password field to load put in password
    try:
        element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "eliloPassword")))
    finally:
        element.send_keys(loginpassword)

    #Wait for login submit button to load and hit the button
    try:
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "loginSubmit")))
    finally:
        driver.find_element_by_id("loginSubmit").click()

    time.sleep(15)

    #Check if there is any ad popup and close it
    if(driver.find_elements_by_xpath("//a[@class='dls-accent-white-01 axp-dynamic-offer__global__closeIcon___1cg6j']")):
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='dls-accent-white-01 axp-dynamic-offer__global__closeIcon___1cg6j']"))).click()

    time.sleep(5)

    #List offer for each card
    while switch == 0:
        nextCard(driver)
        exists = is_element_exist(driver)

        if (exists == True):
            try:
                positionelement = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//a[@data-view-name='ENROLLED']")))
            finally:
                movetoposition(driver, positionelement)
                time.sleep(5)
                positionelement.click()
                time.sleep(5)
                getoffer(driver)
    
    driver.close()


logindetails = {}
f = open(filelocation, "r")
lines = f.readlines()
for x in lines:
    if x != "\n":
        temp = x.split(":")
        logindetails[temp[0].strip()] = temp[1].rstrip("\n").strip()
f.close()


#Save amex offer to all accounts one by one
for logins in logindetails:
    listamexoffer(logins, logindetails[logins])
    position = 0
    switch = 0


# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('C:/WebDriver/AmexOffer.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 0

worksheet.write(row, col, "Card Number")
worksheet.write(row, col + 1, "Offer Brand")
worksheet.write(row, col + 2, "Offer Details")
worksheet.write(row, col + 3, "Offer Expire Date")
row += 1
for data in All_Offers:
    i = 0
    while (i < len(All_Offers[data])):
        worksheet.write(row, col, str(data))
        worksheet.write(row, col + 1, All_Offers[data][i])
        worksheet.write(row, col + 2, All_Offers[data][i+1])
        worksheet.write(row, col + 3, All_Offers[data][i+2])
        i = i + 3
        row += 1

workbook.close()

input('Press Enter to Exit...')
