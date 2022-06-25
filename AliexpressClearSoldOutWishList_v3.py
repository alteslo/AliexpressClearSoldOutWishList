from config import load_config
from cursor import Cursor

config = load_config('./.env')

MY_USER = config.aliexpress.login
MY_PASSWORD = config.aliexpress.password


if __name__ == '__main__':
    cursor = Cursor(MY_USER, MY_PASSWORD, 'chrome', headless=False)
    print(cursor)
    auth = cursor.login()
    cursor.kill_them_all(auth)
