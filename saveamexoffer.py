import re
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

position = 0
switch = 0
TotalOffer = 0
#Text file contain all amex login details
filelocation = "C:/WebDriver/test.txt"
#Location to the firefox web driver
firefoxdriver = "C:/WebDriver/x64/geckodriver.exe"

def is_element_exist(driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a/span[contains(text(),'Amex Offers')]")))
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
    
    time.sleep(5)

    #Click View All in card selection if exists
    if (driver.find_elements_by_xpath("//a[@title='View All']")):
        driver.find_element_by_xpath("//a[@title='View All']").click()

    #Count how many cards
    try:
        element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[@class='dls-accent-white-01-bg border-b dls-accent-gray-01-bg account-row']")))
    finally:
        allcards = driver.find_elements_by_xpath("//*[@class='collapsible-header']")

    #Click on the next card
    if (position < (len(allcards) - 1)):
        allcards[position].click()
        position = position + 1
    else:
        allcards[position].click()
        switch = 1
    time.sleep(7)

def movetoposition(driver, positionelement):
    desired_y = (positionelement.size['height'] / 2) + positionelement.location['y']
    current_y = (driver.execute_script('return window.innerHeight') / 2) + driver.execute_script('return window.pageYOffset')
    scroll_y_by = desired_y - current_y + 150
    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)


def saveoffer(driver):
    global TotalOffer

    #Find if there are offers to save and count how many offers to save
    if(driver.find_elements_by_xpath("//button[@title='Save to Card']")):
        alloffer = driver.find_elements_by_xpath("//button[@title='Save to Card']")
        TotalOffer = int(len(alloffer))

        #Save the offer
        element = driver.find_element_by_xpath("//button[@title='Save to Card']")
        movetoposition(driver, element)
        time.sleep(2)
        element.click()
        time.sleep(3)

        #Scroll the page up
        positionelement = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//a/span[contains(text(),'Amex Offers')]")))
        movetoposition(driver, positionelement)
        time.sleep(5)

        #Click on Avaliable to refresh offer
        element = driver.find_element_by_xpath("//a[@data-view-name='ELIGIBLE']")
        element.click()
        time.sleep(5)
    else:
        TotalOffer = 0


def saveamexoffer(loginname, loginpassword):
    global position
    global switch
    global TotalOffer

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

    #Save each offer to card
    while switch == 0:
        nextCard(driver)
        exists = is_element_exist(driver)

        if (exists == True):
            try:
                positionelement = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//a/span[contains(text(),'Amex Offers')]")))
                element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//a/span[contains(text(),'Available')]")))
            finally:
                movetoposition(driver, positionelement)
                offer_number = element.text[element.text.find("(")+1:element.text.find(")")]
            while ((int(offer_number) != 0) or (int(TotalOffer) != 0)):
                saveoffer(driver)
                time.sleep(2)
                if int(TotalOffer) == 0:
                    break

    print("All Offer Saved")
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
    saveamexoffer(logins, logindetails[logins])
    position = 0
    switch = 0
    TotalOffer = 0

input('Press Enter to Exit...')
