import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from config.data import catalog_pages, BlockVerticalColmun, BlockParseCounter, accountParseCounter, BlockParseInculdeBlocks
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException      
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

class Parsing():

    def __init__(self):

        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options = options
        self.browser = webdriver.Chrome("./chromedriver/chromedriver.exe", options=options)
    def close_browser(self):

        self.browser.close()
        self.browser.quit()

    def pushObjectFunction(self, link, PushObject, CurrentFile):
        with open(f"./info/{CurrentFile}.json", "r") as file:
            data = json.load(file)

        data[f'{link}'] = PushObject

        with open(f"./info/{CurrentFile}.json", "w") as file:
            json.dump(data, file, indent=3)        

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
    def getCurrentPage(self, link):
        browser = self.browser

        browser.get(link)

        
    def update(self, link, CurrentFile):
        browser = self.browser 
        print("HERE")

        if(self.check_exists_by_class("layout-screen") == True):

            # //div[contains(@class, 'main-list')]//child::*
            allElementsArray = [
                "img", # 0
                "product-title",# 1
                "price",# 2
                "buyer-benefits",# 3
                "sku-option sku-actived",# 4
                "sample-list",# 5
                "lead-list",# 6
                "custom-list",# 7
                "ship-list",# 8
                "after-sale-info",# 9
                "Protection",# 10
                "micro-tap-col item-value",# 11
                "micro-tap-row item",# 12
                "product-review", # 13
                "next-form-text-align", # 14
                "quantity-sold", # 15 
                "quality", # 16
                "price-range", # 17 
                "do-entry-item", # 18
                "do-entry-item-val", # 19
                "//div[contains(@class, 'do-entry-separate')]//child::*", # 20
                "review-value", # 21
                "quantity-sold" # 22
            ]



    #""" Overview info """

            ProductDetailArray = []
            ProductDetailTitleArray = []
            ProductPriceArray = []
            ProductPriceTitleArray = []
            ProductReviewsArray = []
            ProductReviewsTitleArray = []
            ProductImageArray = []
            ProductOverviewKeysArray = []
            ProductOverviewValuesArray = []

            # search product detail Keys 
            for elemets_ in browser.find_elements(By.XPATH, allElementsArray[20]):
                CurrentClasses = elemets_.get_attribute("class")
                
                if(CurrentClasses == "attr-name J-attr-name"):
                    ProductOverviewKeysArray.append(elemets_.text)
                                
            # search product detail Values 
            for elemets_ in browser.find_elements(By.XPATH, allElementsArray[20]):
                CurrentClasses = elemets_.get_attribute("class")
                if(CurrentClasses == "do-entry-item-val"):
                    ProductOverviewValuesArray.append(elemets_.text)
                            
            

            # search images
            for elemet_ in browser.find_elements(By.TAG_NAME, allElementsArray[0]):

                loading = elemet_.get_attribute("loading")
                src = elemet_.get_attribute("src")

                if(loading == "lazy"):
                    if(src == "auto"):
                        print("")
                    else:
                        ProductImageArray.append(elemet_.get_attribute("src"))
            
            # search Reviews

            if(self.check_exists_by_id(allElementsArray[13]) == True):

                if(self.check_exists_by_class("next-form-text-align") == True):
                    allReviews = browser.find_element(By.CLASS_NAME, allElementsArray[21])

                    ProductReviewsArray.append(allReviews.text)
                    ProductReviewsTitleArray.append("global_reviews")


                    reviews = browser.find_elements(By.CLASS_NAME, "next-form-text-align")
                    for item in reviews:
                        if(item.get_attribute("class") == "next-form-text-align review-value"):
                            print()
                        else:
                            reviewsText = item.text
                            reviewsReplaceText = reviewsText.replace(' Reviews', '')
                            ProductReviewsTitleArray.append("Reviews")
                            ProductReviewsArray.append(reviewsReplaceText)
                
                if(self.check_exists_by_class(allElementsArray[15]) == True):
                    buyers = browser.find_element(By.CLASS_NAME, allElementsArray[15])
                    buyersText = buyers.text
                    buyersReplaceText = buyersText.replace(' buyer', '')
                    buyersReplaceText = buyersText.replace(' buyers', '')

                    ProductReviewsTitleArray.append("buyers")
                    ProductReviewsArray.append(buyersReplaceText)
                


            # search title
            
            searchTitleChecker = self.check_exists_by_class(allElementsArray[1])

            if(searchTitleChecker == True):
                searchTitleText = browser.find_element(By.CLASS_NAME, allElementsArray[1])
                ProductDetailArray.append(searchTitleText.text)   
                            
                ProductDetailTitleArray.append("product-title")
            # search price
            
            if(self.check_exists_by_class("product-price") == True):
                
                searchPrice = browser.find_elements(By.XPATH, "//div[contains(@class, 'product-price')]//child::*")
                if(self.check_exists_by_class("price-item") == True):
                    for element_ in searchPrice:
                        if(element_.get_attribute("class") == "price"):
                            print(f"Price {element_.text}")
                            print(element_.get_attribute("class"))
                            ProductPriceArray.append(element_.text)

                        elif(element_.get_attribute("class") == "quality"):
                            print(f"quality {element_.text}")
                            print(element_.get_attribute("class"))
                            ProductPriceTitleArray.append(element_.text)
                            

                #ProductPriceArray.append(searchPrice.text)
                
            if(self.check_exists_by_class("product-price") == True):
                
                searchPrice = browser.find_elements(By.CLASS_NAME, "product-price")
                if(self.check_exists_by_class("price-item") == False):
                    for element_ in searchPrice:
                        print(element_.text)

                        ProductPriceArray.append(element_.text)
                            

            # search Benefits

            searchBenefitsChecker = self.check_exists_by_class(allElementsArray[3])

            if(searchBenefitsChecker == True):
                searchBenefitsText = browser.find_element(By.CLASS_NAME, allElementsArray[3])
                ProductDetailArray.append(searchBenefitsText.text)
                ProductDetailTitleArray.append("product-benefits")
                
            # search Model Number

            searchModelChecker = self.check_exists_by_class(allElementsArray[4])

            if(searchModelChecker == True):
                searchModelText = browser.find_element(By.CLASS_NAME, allElementsArray[4])

                ProductDetailArray.append(searchModelText.text)
                ProductDetailTitleArray.append("product-model_number")

            # search samples

            searchSamplesChecker = self.check_exists_by_class(allElementsArray[5])

            if(searchSamplesChecker == True):
                searchSamplesText = browser.find_element(By.CLASS_NAME, allElementsArray[5])

                ProductDetailArray.append(searchSamplesText.text)
                ProductDetailTitleArray.append("product-samples")

            # search Lead time

            searchLeadtimeChecker = self.check_exists_by_class(allElementsArray[6])

            if(searchLeadtimeChecker == True):
                searchLeadtimeText = browser.find_element(By.CLASS_NAME, allElementsArray[6])

                ProductDetailArray.append(searchLeadtimeText.text)
                ProductDetailTitleArray.append("product-lead_time")


            # search Customization

            searchCustomizationChecker = self.check_exists_by_class(allElementsArray[7])

            if(searchCustomizationChecker == True):
                searchCustomizationText = browser.find_element(By.CLASS_NAME, allElementsArray[7])

                ProductDetailArray.append(searchCustomizationText.text)
                ProductDetailTitleArray.append("product-customization")
            
            # search Shipping

            searchShippingChecker = self.check_exists_by_class(allElementsArray[8])

            if(searchShippingChecker == True):
                searchShippingText = browser.find_element(By.CLASS_NAME, allElementsArray[8])

                ProductDetailArray.append(searchShippingText.text)
                ProductDetailTitleArray.append("product-shipping")

            # search Service

            searchServiceChecker = self.check_exists_by_class(allElementsArray[9])

            if(searchServiceChecker == True):
                searchServiceText = browser.find_element(By.CLASS_NAME, allElementsArray[9])

                ProductDetailArray.append(searchServiceText.text)
                ProductDetailTitleArray.append("product-service")

            # search Protection

            searchProtectionChecker = self.check_exists_by_class(allElementsArray[10])

            if(searchProtectionChecker == True):
                searchProtectionText = browser.find_element(By.CLASS_NAME, allElementsArray[10])

                ProductDetailArray.append(searchProtectionText.text)
                ProductDetailTitleArray.append("product-protection")


            # search Protection duble

            searchProtectionDubleChecker = self.check_exists_by_class(allElementsArray[11])

            if(searchProtectionDubleChecker == True):
                searchProtectionDubleText = browser.find_element(By.CLASS_NAME, allElementsArray[11])

                ProductDetailArray.append(searchProtectionDubleText.text)
                ProductDetailTitleArray.append("product-protection_duble")


            
            imageI = 0
            imagect = ProductImageArray.index(ProductImageArray[-1]) + 1

            print(ProductPriceArray)
            priceI = 0 
            pricect = ProductPriceArray.index(ProductPriceArray[-1]) + 1

            overviewI = 0 
            overviewct = ProductOverviewKeysArray.index(ProductOverviewKeysArray[-1]) + 1

            infoCt = ProductDetailTitleArray.index(ProductDetailTitleArray[-1]) + 1
            infoI = 0

            #indices = [i for  in ]

            ProductImages = {}
            ProductPrice = {}
            ProductReviews = {}
            ProductOverview = {}
            ProductUpdateInfo = {}



            while infoI < infoCt:

                ProductUpdateInfo.__setitem__(ProductDetailTitleArray[infoI], ProductDetailArray[infoI])
                
                infoI = infoI + 1   

            while overviewI < overviewct:


                ProductOverview.__setitem__(ProductOverviewKeysArray[overviewI], ProductOverviewValuesArray[overviewI])

                overviewI = overviewI + 1


            while imageI < imagect:

                ProductImages.__setitem__(f"{imageI}", ProductImageArray[imageI])

                imageI = imageI + 1

            while priceI < pricect:
                if ProductPriceTitleArray.__len__():
                    print(ProductPriceTitleArray, pricect, ProductPriceArray)
                    ProductPrice.__setitem__(ProductPriceTitleArray[priceI], ProductPriceArray[priceI])
                else:         
                    ProductPrice.__setitem__("price", ProductPriceArray[priceI])

                
                priceI = priceI + 1


            if(self.check_exists_by_class("quantity-sold") == True):
                print(True)
                reviewsI = 0 
                reviewsct = ProductReviewsArray.index(ProductReviewsArray[-1]) + 1
                
                while reviewsI < reviewsct:

                    ProductReviews.__setitem__(ProductReviewsTitleArray[reviewsI], ProductReviewsArray[reviewsI])
                    reviewsI = reviewsI + 1
            

            PushObject = {
                "Product_Detail": ProductUpdateInfo,
                "Product_Images": ProductImages,
                "Product_Reviews": ProductReviews,
                "Product_Price": ProductPrice,
                "Product_Overview": ProductOverview
            }

            
            self.pushObjectFunction(link=link, PushObject=PushObject, CurrentFile=CurrentFile)

            
        else:
            print("Этот товар пуст")



# 3 13
while True: 
    for key, page in catalog_pages.items():
        CurrentId = page['id']
        CurrentPage = page['url']
        CurrentFile = page['fileName']   
        print(CurrentFile, CurrentPage, CurrentId)
        my_bot = Parsing()

        i = 0
        ct = 1

        while (i < ct):
            with open(f"./info/{CurrentFile}.json", "r") as file:
                files = json.load(file)
                print(CurrentPage)
                for section, commands in files.items():
                    try:
                        my_bot.getCurrentPage(link=section)
                        my_bot.update(link=section, CurrentFile=CurrentFile)
                    except TimeoutException:
                        print("Cannot find product title.")

            i = i + 1      
