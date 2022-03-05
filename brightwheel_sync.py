#!/usr/bin/env python3
# import logging
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import yaml
import datetime
import time

# logging.basicConfig(level=logging.DEBUG)
# my_logger = logging.getLogger(__name__)

def read_configuration(configuration_file = 'config.yaml'):
    with open(configuration_file) as file:
        configuration = yaml.load(file, yaml.FullLoader)
    return configuration


def main():
    configuration = read_configuration()
    driver = webdriver.Firefox(executable_path='./geckodriver')
    driver.get('https://schools.mybrightwheel.com/sign-in')
    time.sleep(2)
    driver.find_element_by_id('username').send_keys(configuration['user'])
    driver.find_element_by_id('password').send_keys(configuration['password'])
    # driver.execute_script()
    # driver.find_element_by_class_name('frontend-acwcvw').click()
    driver.find_element_by_xpath('//button[text()="Sign in"]').click()
    time.sleep(3)


    for kid_name, feed in configuration['feeds'].items():
        driver.get(feed)
        time.sleep(3)
        last_pull = configuration['last_pull'].strftime("%m/%d/%Y")
        driver.find_element_by_id('activity-start-date').send_keys(last_pull, Keys.ENTER)
        driver.find_element_by_id('select-input-2').send_keys('Photo', Keys.ENTER)
        driver.find_element_by_xpath('//button[text()="Apply"]').click()
        load_more = True
        while load_more == True:
            time.sleep(1)
            try:
                driver.find_element_by_xpath('//button[text()="Load more"]').click()
            except:
                load_more = False
        for image in driver.find_elements_by_xpath('//img'):
            image_timestamp = image.get_attribute("src").split('?')[1]
            print(image_timestamp)
            file_name = datetime.datetime.utcfromtimestamp(int(image_timestamp)).strftime("%Y-%m-%d_%H-%M")
            with open(f"{configuration['save_location']}/{kid_name}/{file_name}.png", 'wb') as file:
                file.write(image.screenshot_as_png)
if __name__ == "__main__":
    main()
    pass
