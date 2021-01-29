from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from job import Job
from time import sleep
import random
import sys
import os
import pandas as pd
from datetime import datetime
from tqdm import tqdm


def login(driver: WebDriver):
    try:
        driver.get(os.getenv("HUNTR_BOARD_URL"))
        driver.implicitly_wait(5)
        email_input = driver.find_element_by_xpath("//input[@type='email']")
        password_input = driver.find_element_by_xpath("//input[@type='password']")
        email_input.send_keys(os.getenv("HUNTR_USERNAME"))
        password_input.send_keys(os.getenv("HUNTR_PASSWORD"))
        driver.implicitly_wait(5)
        password_input.send_keys(Keys.ENTER)
        driver.implicitly_wait(5)
        print("Logged In!")
        sleep(1 + random.random() * 4)
    except Exception as err:
        print(f"Error logging in with supplied credentials for "
              f"job board {os.getenv('HUNTR_BOARD_URL')} :" + str(err))
        sys.exit(2)


def get_dict_container(driver: WebDriver) -> dict:
    csv_container = dict()
    try:
        # Populate CSV container keys
        board_headers = driver.find_elements_by_xpath("//input[@class='list-name']")
        for item in board_headers:
            csv_container[item.get_attribute('value')] = None

        return csv_container
    except Exception as err:
        print(f"Error parsing board headers:" + str(err))
        sys.exit(2)


def get_job_items_per_tab(driver: WebDriver, main_container: dict):
    try:
        list_containers = driver.find_elements_by_class_name('list-container')[:-1]
        keys = list(main_container.keys())
        print("Fetching data...")
        for idx in range(len(list_containers)):
            job_list = []
            job_container = list_containers[idx].find_elements_by_tag_name('div')[3]
            job_items = job_container.find_elements_by_tag_name('a')

            for job_item in tqdm(job_items):
                driver.execute_script(f"window.open('{job_item.get_attribute('href')}', '_blank');")
                windows = driver.window_handles
                sleep(3)
                driver.switch_to.window(windows[1])
                driver.implicitly_wait(5)

                # create a Job object from form input fields
                company = driver.find_element_by_xpath("//input[@placeholder='Company']").get_attribute('value')
                job_title = driver.find_element_by_xpath("//input[@placeholder='+ add title']").get_attribute('value')
                location = driver.find_element_by_xpath("//input[@placeholder='+ add location']").get_attribute('value')
                description = driver.find_element_by_class_name('ql-editor').text
                post_url = driver.find_element_by_xpath(
                    "//p[@title='Post URL']/following-sibling::div").find_element_by_tag_name('a').get_attribute('href')

                a_job = Job(company, job_title, post_url, location, description)
                job_list.append(a_job.as_dict())
                driver.close()
                driver.switch_to.window(windows[0])

            main_container[keys[idx]] = job_list

    except Exception as err:
        print(f"Error getting job_container:" + str(err))
        sys.exit(2)


def export_data_to_excel(data: dict):
    try:
        df = pd.DataFrame.from_dict(data, orient='index').transpose()
        out_file = datetime.now().strftime("%d-%m-%Y") + "_out"
        df.to_csv(out_file+".csv", index=False)
        df.to_excel(out_file+".xlsx", engine='xlsxwriter')
    except Exception as err:
        print(f"Error creating outfile:" + str(err))
        sys.exit(2)


def check_environment_vars():
    if 'HUNTR_BOARD_URL' and 'HUNTR_USERNAME' and 'HUNTR_PASSWORD' and 'WEBDRIVER_PATH' not in os.environ:
        print('Please populate .env file with instructions from .env.sample')
        sys.exit(2)


def set_chrome_options(env: str) -> Options:
    """
    Method to set up Webdriver with Chrome options
    :param env: environment being run in dev/prod etc.
    :return: Options object for Chrome webdriver
    """
    chrome_options = Options()

    if env == "dev":
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--window-size=1920,1080")  # use this for debugging on Windows
    else:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")

    return chrome_options


def initialize_driver():
    driver = webdriver.Chrome(os.getenv("WEBDRIVER_PATH"), options=set_chrome_options(os.getenv("ENVIRONMENT")))
    return driver


def main():
    # load config
    load_dotenv()
    check_environment_vars()

    # init driver
    driver = initialize_driver()

    # create dict from board data
    login(driver)
    main_container = get_dict_container(driver)
    get_job_items_per_tab(driver, main_container)
    export_data_to_excel(main_container)


if __name__ == '__main__':
    main()
