from bs4 import BeautifulSoup
from selenium.webdriver import Keys
import requests
import time
from datetime import datetime


class ImotBgSearch:
    def __init__(self, driver, url, google_form_url):
        self.driver = driver
        self.url = url
        self.google_form_url = google_form_url
        self.today = datetime.today().date()

    def find_listings(self):
        self.driver.get(self.url)
        time.sleep(1)
        self.driver.find_element_by_xpath('/html/body/div[6]/div[2]/div[1]/div[2]/div[2]/button[1]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="BG-23"]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="formFastSearch"]/div[1]/a[1]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="vi3"]').click()
        self.driver.find_element_by_xpath('//*[@id="vi4"]').click()
        max_price = self.driver.find_element_by_xpath('/html/body/div[1]/form/table[1]/tbody/tr[1]/td[2]/table[1]'
                                                      '/tbody/tr[2]/td[3]/input')
        max_price.click()
        time.sleep(1)
        max_price.send_keys(700)
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="ri"]/optgroup[6]/option[4]').click()
        self.driver.find_element_by_xpath('/html/body/div[1]/form/table[2]/tbody/tr/td[2]/table[1]'
                                          '/tbody/tr[2]/td[2]/img[1]').click()
        self.driver.find_element_by_xpath('//*[@id="ri"]/optgroup[3]/option[7]').click()
        self.driver.find_element_by_xpath('/html/body/div[1]/form/table[2]/tbody/tr/td[2]/table[1]'
                                          '/tbody/tr[2]/td[2]/img[1]').click()
        self.driver.find_element_by_xpath('//*[@id="ri"]/optgroup[17]/option[5]').click()
        self.driver.find_element_by_xpath('/html/body/div[1]/form/table[2]/tbody/tr/td[2]/table[1]'
                                          '/tbody/tr[2]/td[2]/img[1]').click()
        self.driver.find_element_by_xpath('/html/body/div[1]/form/table[1]/tbody/tr[1]'
                                          '/td[2]/table[2]/tbody/tr[3]/td[3]/input').click()
        time.sleep(5)
        self.driver.find_element_by_xpath('//*[@id="clever_50997_pushdown_close"]').click()
        time.sleep(5)
        query_link = self.driver.find_element_by_xpath('/html/body/div[1]/table[1]/tbody/tr[1]/td[1]/table[1]'
                                                       '/tbody/tr[2]/td/div/input').get_attribute('value')
        time.sleep(1)
        return query_link

    def create_properties_dictionary(self):
        query_link = requests.get(self.find_listings())
        query_link.encoding = "WINDOWS-1251"
        soup = BeautifulSoup(query_link.text, "lxml")

        prices = [price.getText().strip() for price in soup.find_all(class_="price")]
        addresses = [address.getText().split(",")[1].strip() for address in soup.find_all(name="a", class_="lnk2")]
        urls = [url["href"].split("//")[1].strip() for url in soup.find_all(class_="lnk2", href=True)]

        properties_dictionary = {}
        for n in range(len(prices)):
            properties_dictionary[f"Property {n + 1}"] = {
                "price": prices[n],
                "address": addresses[n],
                "url": urls[n]
            }
        return properties_dictionary

    def login_to_google(self):
        self.driver.get(self.google_form_url)
        time.sleep(3)
        click_here = self.driver.find_element_by_xpath('//*[@id="SMMuxb"]/a[1]')
        click_here.click()
        time.sleep(3)

        google_login_window = self.driver.window_handles[1]
        self.driver.switch_to.window(google_login_window)
        time.sleep(3)

        email_field = self.driver.find_element_by_xpath('//*[@id="identifierId"]')
        email_field.click()
        time.sleep(1)

        email_field.send_keys("EMAIL")
        email_field.send_keys(Keys.ENTER)
        time.sleep(3)

        password_field = self.driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
        password_field.send_keys("PASSWORD")
        password_field.send_keys(Keys.ENTER)
        time.sleep(3)

    def fill_google_form(self, address, price, url):
        self.driver.get(self.google_form_url)
        time.sleep(3)
        address_input = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]'
                                                          '/div/div/div[2]/div/div[1]/div/div[1]/input')
        price_input = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]'
                                                        '/div/div/div[2]/div/div[1]/div/div[1]/input')
        link_input = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]'
                                                       '/div/div/div[2]/div/div[1]/div/div[1]/input')
        submit_button = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]'
                                                          '/div[1]/div[1]/div/span')
        time.sleep(1)
        address_input.send_keys(address)
        time.sleep(1)
        price_input.send_keys(price)
        time.sleep(1)
        link_input.send_keys(url)
        time.sleep(1)
        submit_button.click()
        time.sleep(3)
        return_back = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
        return_back.click()
        time.sleep(1)

    def create_the_table(self):
        time.sleep(3)
        edit_form = self.driver.find_element_by_xpath('/html/body/div/div[1]/div/span')
        edit_form.click()
        time.sleep(3)
        answers = self.driver.find_element_by_xpath('//*[@id="tJHJj"]/div[3]/div[1]/div/div[2]/span/div')
        answers.click()
        time.sleep(3)
        create_table = self.driver.find_element_by_xpath('//*[@id="ResponsesView"]/div/div[1]/div[1]'
                                                         '/div[2]/div[1]/div/div/span/span/div/div[1]')
        create_table.click()
        time.sleep(3)
        table_name = self.driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[9]/div/div[2]/span/div/div/span/div[1]'
                                                       '/div/div/div[1]/div/div[1]/input')
        table_name.click()
        time.sleep(1)
        table_name.send_keys(Keys.COMMAND + "a")
        table_name.send_keys(Keys.BACK_SPACE)
        time.sleep(1)
        table_name.send_keys(f"Properties_{self.today}")
        time.sleep(1)
        create_button = self.driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[9]/div/div[2]/div[3]/div[2]/span/span')
        create_button.click()
        time.sleep(10)
        self.driver.close()

