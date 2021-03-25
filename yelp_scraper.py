from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import json
import sys
import cv2
# from fer import FER
from flask_restful import Resource, Api, reqparse


url = 'https://www.yelp.com/biz/spiral-pasay-2'
chrome_driver_path = '/Users/mac/PycharmProjects/chromedriver'

chrome_options = Options()
chrome_options.add_argument('--headless')

webdriver = webdriver.Chrome(
    executable_path=chrome_driver_path, options=chrome_options
)


class Scrape(Resource):
    def scrape_yelp(self):

        if len(sys.argv) >= 2:
            search_query = sys.argv[1]
            print(search_query)

        with webdriver as driver:
            # Set timeout time
            wait = WebDriverWait(driver, 10)

            # retrieve url in headless browser
            driver.get(url)
            reviews_arr = []
            i_reviewer = {}
            result = []
            final_reviews = []

            reviewers = driver.find_elements_by_xpath("//a[contains(@href, '/user')]")
            reviews = driver.find_elements_by_xpath("//span[contains(@class, 'raw__373c0__3rcx7')"
                                                    "and contains(@lang, 'en')]")
            avatars = driver.find_elements_by_xpath("//a[contains(@href, '/user')]//"
                                                    "img[contains(@class, 'photo-box-img__373c0__35y5v')]")

            for review in reviews:
                r_a = review.text.split('\n')
                reviews_arr.append(r_a)

            for r in reviews_arr:
                review_a = r
                final_reviews.append(review_a)

            for reviewer in reviewers:
                i_reviewer.clear()
                reviewer_a = reviewer.text.split('\n')
                if reviewer_a[0] == '':
                    continue
                else:
                    result.append({"reviewer": reviewer_a[0], "review": "myreview"})

                # for v in final_reviews:
                #     review_a = v
                    # result.append({"review": review_a})
                    # result.append({"review": "myreviewtest"})

            # detector = FER()

            for index, av in enumerate(avatars, start=0):
                result[index]["avatar"] = av.get_attribute("src")
                # img = cv2.imread(av.get_attribute("src"))
                # emotion, score = detector.top_emotion(img)
                # print(emotion)

            # must close the driver after task finished
            driver.close()
            json_res = json.dumps(result)
            return json_res
