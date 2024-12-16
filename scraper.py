from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException, StaleElementReferenceException
import pandas as pd
import time

CHROME_DRIVER = 'C:/Users/ibrah/Downloads/chromedriver-win64/chromedriver.exe'

WEB_LINK = 'https://www.opentable.com/blacksalt?originId=8e3d9fe3-8757-46ab-b6be-79f1e84dda59&corrid=8e3d9fe3-8757-46ab-b6be-79f1e84dda59&avt=eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ'

#open driver service
service = Service(executable_path=CHROME_DRIVER)
try:
    scraper = webdriver.Chrome(service=service)
    scraper.get(WEB_LINK)
except ValueError as e:
    print(f"Error: {e}")
    print("Please ensure the ChromeDriver path")

reviewer_name = []
diner_review = []
overall_rating = []
food_rating = []
service_rating = []
ambiance_rating = []

ratings = []

def scraper_func():
    reviews = scraper.find_elements(by='xpath', value = '//li[contains(@class, "afkKaa-4T28-")]')
    for review in reviews:
        reviewer_name.append(review.find_element(by = 'xpath', value = './/p[contains(@class, "_1p30XHjz2rI-")]').text)
        diner_review.append(review.find_element(by = 'xpath', value = './/span[contains(@class, "l9bbXUdC9v0-")]').text)
        ratings_element = review.find_elements(by = 'xpath', value = './/span[contains(@class, "-y00OllFiMo-")]')

        ratings = [rating.text for rating in ratings_element]

        if len(ratings) == 4:
            overall_rating.append(ratings[0])
            food_rating.append(ratings[1])
            service_rating.append(ratings[2])
            ambiance_rating.append(ratings[3])


while True:
    scraper_func()

    try:
        next_page_link = scraper.find_elements(by='xpath', value='//a[contains(@aria-label, "Go to the next page")]')
        if next_page_link:
            try:
                next_page_link[0].click()  # Click on the first element in the list
                time.sleep(2)  # Wait for the page to load
            except StaleElementReferenceException:
                time.sleep(2)  # Wait and retry
                next_page_link = scraper.find_elements(by='xpath', value='//a[contains(@aria-label, "Go to the next page")]')
                if next_page_link:
                    next_page_link[0].click()
                else:
                    break
        else:
            break  # Exit the loop if there is no next page link
    except NoSuchElementException:
        break
    



data_raw = pd.DataFrame({
                            'Name':reviewer_name, \
                            'Review_raw':diner_review, \
                            'Overall': overall_rating, \
                            'Food': food_rating, \
                            'Service': service_rating, \
                            'Ambiance':ambiance_rating
                        })
data_raw.to_csv('review_data.csv', index = True)


scraper.quit()
