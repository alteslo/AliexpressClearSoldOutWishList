from time import sleep

from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

from driver import Driver_config


class Cursor:
    """
    Cursor object that allows you to interact with the Aliexpress wishlist.
    It takes three required arguments: login, password,
    and web driver (chrome or firefox).
    The login must be the first method.
    """
    ALI_URL = 'https://login.aliexpress.ru/'
    ALI_WISH_URL = 'https://my.aliexpress.ru/wishlist/' \
                   + 'wish_list_product_list.htm?currentGroupId=0'

    def __init__(self, user, password, browser, headless=True):
        self.user = user
        self.password = password
        self.headless = headless
        if browser not in ['chrome', 'firefox']:
            raise ValueError('browser must be only firefox or chrome')
        self.browser = browser

    @property
    def driver(self):
        driver_config = Driver_config()

        if self.browser == 'firefox':
            driver_config = driver_config.firefox
        else:
            driver_config = driver_config.chrome

        web_driver = driver_config.driver
        service = driver_config.service
        manager = driver_config.manager

        if self.headless:
            options = driver_config.options
            options.add_argument("--headless")
            driver = web_driver(
                service=service(manager.install()),
                options=options
            )
            return driver
        driver = web_driver(
            service=service(manager.install())
        )
        return driver

    def login(self):
        """
        Authorize and returns True if success or False if not
        """
        driver = self.driver
        driver.get(Cursor.ALI_URL)

        try:
            wait = WebDriverWait(driver, 30)
            wait.until(
                EC.presence_of_element_located((By.ID, "email"))
            )
        except Exception:
            return False

        else:
            login = driver.find_element(By.ID, 'email')
            login.send_keys(self.user)
            sleep(2)
            password = driver.find_element(By.ID, 'password')
            password.send_keys(self.password)
            sleep(2)
            driver.find_element(
                By.XPATH,
                '/html/body/div/div/div[3]/div/div[1]/div[3]/div/form/button'
            ).click()
            sleep(1)
            driver.switch_to.default_content()
        return True

    @staticmethod
    def _load_all_items(driver):
        while True:
            try:
                button_load_more = driver.find_element(
                    By.CLASS_NAME,
                    'Wishlist_ButtonLoadMore__loadMoreBtn__zjmf8'
                )
                button_load_more.click()
            except exceptions.NoSuchElementException:
                break

    def kill_them_all(self, auth):
        """
        Completely clears the wishlist
        """
        driver = self.driver
        driver.get(Cursor.ALI_WISH_URL)
        sleep(5)
        if auth:
            self._load_all_items(driver)

            links = driver.find_elements_by_class_name(
                'Wishlist_ActionBlock__delete__1mups'
            )

            if len(links) == 0:
                print('Ваш wishlist уже пуст')
            else:
                print(f'Количество предметов в списке жеданий {len(links)}')
                actions = ActionChains(driver)
                for link in tqdm(links):
                    actions.move_to_element(link)
                    actions.click(link)
                    actions.perform()
        else:
            raise Exception('Please check your credentials')

    def bury_only_the_dead(self):
        """
        Clear wishlist from...
        """
        pass
