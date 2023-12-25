import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class extractReviews:
    def __init__(self,driver):
        self.driver = driver
    def mostCommon(self,numReviews=0):
        time.sleep(2)
        try:
            openReview = self.driver.find_element(By.CSS_SELECTOR,
                                             'button[role="tab"][class="hh2c6 "][aria-label*="Reviews"]')
            openReview.click()
            time.sleep(0.5)
        except:
            pass

        i = 0
        while i < 2:
            elem = self.driver.find_element(By.CSS_SELECTOR, 'div[class="m6QErb DxyBCb kA9KIf dS8AEf "]')
            elem.send_keys(Keys.END)
            time.sleep(0.5)

            i += 1

        time.sleep(0.5)
        MoreButton = self.driver.find_elements(By.XPATH,
                                               "//button[contains(text(), 'More')]")
        i = 0
        while i < numReviews + 10:
            MoreButton[i].send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)
            try:
                MoreButton[i].click()
            except:
                pass
            i += 1
        reviews = []

        i = 0
        while i < numReviews:
            review = self.driver.find_elements(By.CSS_SELECTOR, 'span[class="wiI7pd"]')[i]
            reviews.append(review.text)
            i += 1

        return reviews
    def newest(self,url,numReviews=0):
        time.sleep(2)
        self.driver.get(url)

        openReview = self.driver.find_element(By.CSS_SELECTOR,
                                         'button[role="tab"][class="hh2c6 "][aria-label*="Reviews"]')
        openReview.click()

        try:
            time.sleep(1)
            sortButton = self.driver.find_element(By.XPATH,
                                             "//div[contains(text(), 'Most relevant')]")
            sortButton.click()
            time.sleep(0.5)
            HighestRating = self.driver.find_element(By.CSS_SELECTOR,
                                             'div[jsinstance="1"][data-index="1"]')
            HighestRating.click()
        except:
            pass

        time.sleep(0.5)
        reviews = []

        i = 0
        while i < 2:
            elem = self.driver.find_element(By.CSS_SELECTOR, 'div[class="m6QErb DxyBCb kA9KIf dS8AEf "]')
            elem.send_keys(Keys.END)
            time.sleep(0.5)

            i += 1

        time.sleep(0.5)
        MoreButton = self.driver.find_elements(By.XPATH,
                                               "//button[contains(text(), 'More')]")
        i = 0
        while i < numReviews + 10:
            MoreButton[i].send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)
            try:
                MoreButton[i].click()
            except:
                pass
            i += 1

        i = 0
        while i < numReviews:
            review = self.driver.find_elements(By.CSS_SELECTOR, 'span[class="wiI7pd"]')[i]
            reviews.append(review.text)
            i += 1

        return reviews
