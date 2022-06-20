from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Cursor():
    ALI_URL = 'https://login.aliexpress.ru/'
    ALI_WISH_URL = 'https://my.aliexpress.com/wishlist/wish_list_product_list.htm?&currentGroupId=0&page='

    def __init__(self, user, password, headless=True):
        self.user = user
        self.password = password
        self.headless = headless

    @property
    def __driver(self):
        if self.headless:
            options = FirefoxOptions()
            options.add_argument("--headless")
            return webdriver.Firefox(options=options)
        return webdriver.Firefox()

    def __load_web_page(self, url):
        return self.__driver.get(url)

    def login(self):
        driver = self.__load_web_page(Cursor.ALI_URL)
        sleep(5)
        element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "fm-login-id")))
        element = driver.find_element(By.ID, 'fm-login-id')
        element.send_keys(self.user)
        element = driver.find_element(By.ID, 'fm-login-password')
        element.send_keys(self.password)
        driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div/div/div[3]/div/button").click()
        driver.switch_to.default_content()
        # return True

    def kill_them_all(self):
        driver = self.__load_web_page(Cursor.ALI_URL)

        for i in tqdm(range(1, 51, 1)):  # 50 pages for wishlist
            driver.get(Cursor.ALI_WISH_URL + str(i))  # you may set group id for u wishlist
            links = driver.find_elements(By.XPATH, (
                '/html/body/div[4]/div[2]/div/div[2]/div[2]/ul/li[@class="product sold-out util-clearfix js-product"]/div['
                '2]/p/a'))

            urls = [link.get_attribute("href") for link in links]
