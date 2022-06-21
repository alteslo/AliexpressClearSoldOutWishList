from time import sleep

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager


class Cursor:
    ALI_URL = 'https://login.aliexpress.ru/'
    ALI_WISH_URL = 'https://my.aliexpress.ru/wishlist/wish_list_product_list.htm?currentGroupId=0'

    def __init__(self, user, password, headless=True):
        self.user = user
        self.password = password
        self.headless = headless

    @staticmethod
    def __get_driver(headless):
        if headless:
            options = ChromeOptions()
            options.add_argument("--headless")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            return driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        return driver

    def login(self):
        driver = Cursor.__get_driver(self.headless)
        # self.driver = driver
        driver.get(Cursor.ALI_URL)

        try:
            wait = WebDriverWait(driver, 30)
            wait.until(
                EC.presence_of_element_located((By.ID, "fm-login-id"))
            )
        finally:
            login = driver.find_element(By.ID, 'fm-login-id')
            login.send_keys(self.user)

            password = driver.find_element(By.ID, 'fm-login-password')
            password.send_keys(self.password)

            driver.find_element(
                By.XPATH, '/html/body/div[1]/div/div[3]/div/div[1]/div[3]/div/button'
            ).click()
            driver.switch_to.default_content()
            self.driver = driver
        return True

    def kill_them_all(self):
        sleep(5)
        driver = self.driver
        driver.get(Cursor.ALI_WISH_URL)

        while True:
            try:
                button_load_more = driver.find_element(By.CLASS_NAME, 'Wishlist_ButtonLoadMore__loadMoreBtn__zjmf8')
                button_load_more.click()
            except exceptions.NoSuchElementException:
                break

        links = driver.find_elements_by_class_name('Wishlist_ActionBlock__delete__1mups')

        print(f'Количество предметов в списке жеданий {len(links)}')
        actions = ActionChains(driver)
        for link in tqdm(links):
            # actions.move_to_element(link)
            actions.click(link)


        
        # for i in tqdm(range(1, 51, 1)):  # 50 pages for wishlist
        #     # you may set group id for u wishlist
        #     driver.get(Cursor.ALI_WISH_URL + str(i))
        #     links = driver.find_elements(By.XPATH, (
        #         '/html/body/div[4]/div[2]/div/div[2]/div[2]/ul/li[@class="product sold-out util-clearfix js-product"]/div['
        #         '2]/p/a'))

        #     urls = [link.get_attribute("href") for link in links]
        
        # for u in tqdm(urls):
        #     print(u)
        #     driver.get(u)
