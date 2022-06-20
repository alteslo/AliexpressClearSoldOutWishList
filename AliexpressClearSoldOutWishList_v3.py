from tqdm import tqdm

from misc import Cursor
from config import load_config

config = load_config('./.env')

MY_USER = config.aliexpress.login
MY_PASSWORD = config.aliexpress.password


cursor = Cursor(MY_USER, MY_PASSWORD, headless=False)
login = cursor.login()

if login:
    cursor.kill_them_all()





# if __name__ == '__main__':
#     try:
#         asyncio.run(main())
#     except (KeyboardInterrupt, SystemExit):
#         logger.error("Bot stopped!")

for u in tqdm(urls):
    print(u)
    driver.get(u)
