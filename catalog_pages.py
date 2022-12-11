import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from config.data import catalog_pages, getPages
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException      
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions




class Parsing():

    def __init__(self):

        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--start-maximized")
        options = options
        self.browser = webdriver.Chrome("./chromedriver/chromedriver.exe", options=options)

    def close_browser(self):

        self.browser.close()
        self.browser.quit()

    def login(self, CurrentPage):

        browser = self.browser

        browser.get(CurrentPage)
        time.sleep(0.30)

    def check_exists_by_xpath(self, xpath):
        browser = self.browser 

        try:
            browser.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    def check_exists_by_class(self, className):
        browser = self.browser 

        try:
            browser.find_element(By.CLASS_NAME, className)
        except NoSuchElementException:
            return False
        return True
    
    def check_exists_by_id(self, id):
        browser = self.browser 

        try:
            browser.find_element(By.ID, id)
        except NoSuchElementException:
            return False
        return True

    def pushObjectFunction(self, link, PushObject, CurrentFile):
        with open(f"./info/Links{CurrentFile}.json", "r") as file:
            data = json.load(file)
        data[f'{link}'] = PushObject

        with open(f"./info/Links{CurrentFile}.json", "w") as file:
            json.dump(data, file, indent=3)        
   

    def error(self, error, PushObject):
        with open(f"./info/Error.json", "r") as file:
            data = json.load(file)
            print(data)
        data[f'{error}'] = PushObject

        with open(f"./info/Error.json", "w") as file:
            json.dump(data, file, indent=3)        

    def getCartProfile(self):
        browser = self.browser
        key = 0
        print(CurrentFile)
        while key < getPages:
            
            browser.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(2)
            key+=1

        if CurrentFile == "file13":
            time.sleep(5)

        if(self.check_exists_by_class("recommend-list-content")):
            print("1 here")

            catalog = browser.find_elements(By.XPATH, "//div[contains(@class, 'recommend-list-content')]//child::*")


            for element_ in catalog:
                if(element_.get_attribute("class") == "dx-event-node"):
                    browser.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                    url = element_.get_attribute("href")

                    print(url[:url.find('?spm=')])
                    self.pushObjectFunction(url[:url.find('spm=')], {}, CurrentFile)

        elif(self.check_exists_by_class("listbase")):
            print("2 here")
            catalog = browser.find_elements(By.XPATH, "//div[contains(@class, 'listbase common-product-list')]//child::*")

            for element_ in catalog:
                if(element_.get_attribute("class") == "product-detail"):

                    url = element_.get_attribute("href")
                    print(url[:url.find('?spm=')])
                    self.pushObjectFunction(url[:url.find('spm=')], {}, CurrentFile)
                    # browser.find_element(By.TAG_NAME, "body").send_keys(Keys.END)

        else:
            print("Error")
            self.error(f"Error", {"error": f"ElementLink not found, in page {CurrentPage}"})




for key, page in catalog_pages.items():
    
    CurrentId = page['id']
    CurrentPage = page['url']
    CurrentFile = page['fileName']   
    print(CurrentPage)
    
    my_bot = Parsing()
    my_bot.login(CurrentPage)
    my_bot.getCartProfile()
    my_bot.close_browser()



