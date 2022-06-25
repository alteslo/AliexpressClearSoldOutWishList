## AliexpressClearSoldOutWishList

This is a Python script that uses Selenium with Chrome or Firefox to clear user Wish List in different cases
hope that helps you

### Functionality
- Complete cleaning of the wish list
- Clearing a sold out item in the wish list (coming soon)

### Interesting
- There is no need to install the web driver special

### Warning!!!
- Aliexpress regularly makes changes to its html structure. And also uses a captcha. Therefore, at some point this tool will need updating

### Tools
- Python >= 3.9
- Selenium

## Старт

#### 1) Rename "api\api\.env copy" на "api\api\.env" and register your credentials

    LOGIN = 'your_name'
    PASSWORD = 'your_password'

#### 2) Installing the required packages

    pip install -r requirements.txt

##### 3) Edit the file AliexpressClearSoldOutWishList.py according to your task. At the moment, the file runs a script to completely clear the wish list.

    if __name__ == '__main__':
        cursor = Cursor(MY_USER, MY_PASSWORD, 'chrome', headless=False)
        auth = cursor.login()
        cursor.kill_them_all(auth)

##### 4) Run AliexpressClearSoldOutWishList.py
    python AliexpressClearSoldOutWishList.py
