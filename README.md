# AU-Save-Amex-Offer
Python Script to auto save amex offer

Modifier this part in the code to the location of your Firefox x64 WebDriver
driver = webdriver.Firefox(executable_path=r"C:/WebDriver/x64/geckodriver.exe")

Modifier this part in the code to the location of your account login username:password text file
filelocation = "C:/WebDriver/amexaccounts.txt"

In the login text file format is
username1:password1
username2:password2
username3:password3
You can put as many as you want

Prerequisite:
Install Python 3
Install Selenium
Go to this link https://github.com/mozilla/geckodriver/releases to download firefox WebDriver
