import datetime
import json
import os
import time

from selenium import webdriver

import settings
from fetch_recipt import FetchAmazonRecipt

if __name__ == '__main__':
    obj = FetchAmazonRecipt()
    driver = obj.setting_driver()
    driver.get("https://www.amazon.co.jp/")
    obj.login(driver)
    obj.collect_recipt(driver)
