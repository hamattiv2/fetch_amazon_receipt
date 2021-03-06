import datetime
import json
import os
import time
import math
import glob
import shutil

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

import settings

class FetchAmazonRecipt(object):
    def __init__(self):
        self.user_id = settings.user_id
        self.password = settings.password
        self.download_path = settings.download_path
        self.save_path = settings.save_path
        self.collect_year = settings.collect_year

    def setting_driver(self):
        """Amazonにアクセスするためのドライバを設定する"""
        chrome_options = webdriver.ChromeOptions()
        settings = {'recentDestinations': 
                        [
                            {
                                'id': 'Save as PDF',
                                'origin': 'local',
                                'account': ''
                            }
                        ],
                        'selectedDestinationId': 'Save as PDF', 
                        'version': 2
                    }
        prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument('--kiosk-printing')
        return webdriver.Chrome('chromedriver.exe', options=chrome_options)

    def login(self, driver):
        """Amazonにログインする"""
        driver.find_element_by_id('nav-link-accountList').click()
        driver.find_element_by_id('ap_email').send_keys(self.user_id)
        driver.find_element_by_id('continue').click()
        driver.find_element_by_id('ap_password').send_keys(self.password)
        driver.find_element_by_id('signInSubmit').click()
        time.sleep(1)

    def collect_recipt(self, driver):
        """領収書を収集する"""
        driver.get(f'https://www.amazon.co.jp/gp/your-account/order-history?orderFilter=year-{self.collect_year}')
        pages = math.ceil(int(driver.find_element_by_class_name('num-orders').text[0: -1]) / 10)
        pages += 1

        for page in range(pages):
            if page == 0:
                pass
            else:
                driver.switch_to.window(driver.window_handles[0])
                next_page = page + 1
                driver.get(f'https://www.amazon.co.jp/gp/your-account/order-history/ref=ppx_yo_dt_b_pagination_{ page }_{ next_page }?ie=UTF8&orderFilter=year-2020&search=&startIndex={ page }0')

            item_list = driver.find_elements_by_tag_name('bdi')
            item_list = [item.text for item in item_list]
            for item in item_list:
                driver.switch_to.window(driver.window_handles[0])
                driver.execute_script("window.open()")
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[-1])
                
                try:
                    driver.get(f'https://www.amazon.co.jp/gp/digital/your-account/order-summary.html/ref=oh_aui_ajax_dpi?ie=UTF8&orderID={ item }&print=1')
                    driver.execute_script('window.print();')
                    new_filename = driver.find_element_by_class_name('h1').text + '.pdf'
                except:
                    file = glob.glob(f"{ self.download_path }/*.pdf")[0]
                    try:
                        os.remove(file)
                    except:
                        pass
                    driver.get(f'https://www.amazon.co.jp/gp/css/summary/print.html/ref=oh_aui_ajax_invoice?ie=UTF8&orderID={ item }')
                    driver.execute_script('window.print();')
                    new_filename = driver.find_element_by_class_name('h1').text + '.pdf'
                print(new_filename)
                file = glob.glob(f"{ self.download_path }/*.pdf")[0]
                shutil.move(file, f'{ self.save_path }/{ new_filename }')
                driver.close()
        driver.close()