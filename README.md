# A Python Script to Auto Save Amex Offer (AU)

## Description

saveamexoffer.py - For Auto Save Offers

listamexoffer.py - Export Saved Offer to Excel Sheet


## Installation

1. [Install Python 3](https://www.python.org/downloads/)
2. Go to this [link](https://github.com/mozilla/geckodriver/releases) to download firefox WebDriver
3. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Selenium.
      ```bash
      pip install selenium
      ```
4. Install xlsxwriter
      ```bash
      pip install XlsxWriter
      ```

## Usage

```python

#Modify this part of the code to the location of your Firefox x64 WebDriver

firefoxdriver = "C:/WebDriver/x64/geckodriver.exe"

#Modify this part of the code to the location of your account login username:password text file

filelocation = "C:/WebDriver/amexaccounts.txt"

```

Sample login text file format

```
username1:password1
username2:password2
username3:password3
```

