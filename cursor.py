from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

from driver import Driver_config


class Cursor:
    """
    Cursor object that allows you to interact with the Aliexpress wishlist
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
        if self.headless:
            options = FirefoxOptions()
            options.add_argument("--headless")
            driver = webdriver.Firefox(
                service=Service(GeckoDriverManager().install()),
                options=options
            )
            return driver
        driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install())
        )
        return driver

    def login(self):
        """
        Authorize and returns True if success
        """
        driver = self.driver
        driver.get(Cursor.ALI_URL)

        try:
            wait = WebDriverWait(driver, 30)
            wait.until(
                EC.presence_of_element_located((By.ID, "fm-login-id"))
            )
        except Exception:
            return False

        else:
            login = driver.find_element(By.ID, 'fm-login-id')
            login.send_keys(self.user)
            password = driver.find_element(By.ID, 'fm-login-password')
            password.send_keys(self.password)

            driver.find_element(
                By.XPATH,
                '/html/body/div[1]/div/div[3]/div/div[1]/div[3]/div/button'
            ).click()
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
