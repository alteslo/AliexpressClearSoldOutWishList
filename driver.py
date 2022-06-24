from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as F_Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as G_Service
from webdriver_manager.chrome import ChromeDriverManager

from dataclasses import dataclass


@dataclass
class Firefox:
    options = FirefoxOptions
    driver = webdriver.Firefox
    service = F_Service
    manager = GeckoDriverManager


@dataclass
class Chrome:
    options = ChromeOptions
    driver = webdriver.Chrome
    service = G_Service
    manager = ChromeDriverManager


@dataclass
class Driver_config:
    chrome = Chrome
    firefox = Firefox
