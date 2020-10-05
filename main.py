import glob
import time
import csv
from multiprocessing import Manager, Pool
from bs4 import BeautifulSoup
from loguru import logger
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import requests
import unidecode
import config


# Empty values for multiprocessing
MANAGER = []
SHARED_LIST = []

# LOGURU INITIALIZE
logger.add('info.log', format='{time} {level} {message}',
            level='INFO', rotation="1 MB", compression='zip')


@logger.catch
def region_extractor(page) -> list:
    """
    From a start page looking for a regions to be scraped
    """
    soup = BeautifulSoup(page.text, 'lxml')
    countries = []
    region_div = soup.find('div', class_=config.REGION_DIV_CLASS)
    for match in region_div.find_all('li', class_=config.REGION_LI_CLASS):
        coutry_link = match.a.get('href')
        countries.append(coutry_link)
    return countries


@logger.catch
def activities_page_extractor(browser) -> list:
    """
    From page extracts all articles of activities
    """
    activities_list = []
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    for activity in soup.find_all('article',
                                class_=config.ACTIVITY_ARTICLE_CLASS):
        activity_link = config.START_URL[:-1] + activity.a.get('href')
        activities_list.append(activity_link)
    return activities_list


@logger.catch
def activity_info_extractor(*args):
    """
    (LAUNCHES IN MULTIPROCCESING)
    From each activity page scrapes all needed information and then
    adding to the SHARED_LIST of processes
    """
    for activity in args:
        time.sleep(config.TIME_DELAY)
        soup = BeautifulSoup(requests.get(activity).text, 'lxml')

        for element in soup.select(config.TITLE_SELECTOR):
            # Decodes as there could be German/French letters
            title = unidecode.unidecode(element.get_text())

        for element in soup.select(config.CATEGORY_SELECTOR):
            category = element.get_text()

        for element in soup.select(config.LOCATION1_SELECTOR):
            # Decodes as there could be German/French letters
            location1 = unidecode.unidecode(element.get_text())

        for element in soup.select(config.LOCATION2_SELECTOR):
            # Decodes as there could be German/French letters
            location2 = unidecode.unidecode(element.get_text())
        final_location = location1 + ', ' + location2

        link_element = soup.find_all('a', class_=config.LINK_BUTTON_CLASS)[1]
        link = link_element.get('href')

        SHARED_LIST.append({'title': title, 'category': category,
                            'location': final_location, 'website': link})

        logger.info(f"{title} activity has been scraped")


@logger.catch
def save_csv(shared_list: list, country: str):
    """
    Saves collected data to .csv
    """
    with open('results/' + country + '.csv', mode='w', newline='') as csv_file:
        fieldnames = ['title', 'category', 'location', 'website']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in shared_list:
            writer.writerow(row)
    csv_file.close()


@logger.catch
def activities_funnel(country: str):
    """
    Launches Chrome with country page and executes functions to grab
    all articles through pages and then scrape data of each activity
    """
    # Starts Chrome
    with Chrome(options=config.chrome_options,
                executable_path=config.CHROME_DRIVER_PATH) as browser:
        browser.get(country)
        # Cutting country name from link to create name of CSV doc
        country_name = country.split('/')[-2]
        # Waits until the page with pagination and articles is loading
        WebDriverWait(browser, 30).until(EC.presence_of_element_located(
                                        (By.XPATH, config.XPATH_PAGINATION)))
        # Searches for a "next page button" in pagination div
        next_page = browser.find_element_by_xpath(config.XPATH_NEXT_PAGE)
        # Scrape first page separetely due to vulnerablity of "while"
        first_page_activities = activities_page_extractor(browser)
        activity_info_extractor(*first_page_activities)
        # Scrapes all pages until "next page button" becomes inactive
        while next_page.is_enabled():
            browser.execute_script("arguments[0].click();", next_page)
            next_page_activities = activities_page_extractor(browser)
            activity_info_extractor(*next_page_activities)
            # After all result received writing them into csv
            save_csv(SHARED_LIST, country_name)

        logger.info(f"Search has been finishes for {country}")


@logger.catch
def csv_merger():
    """
    Merges all created CSVs to one excel file
    """
    # Searches for CSV files in results folder
    all_filenames = [i for i in glob.glob(f'results/*.{"csv"}')]
    # Combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    # Export to excel
    combined_csv.to_excel( "result.xlsx", index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    # Launching a multiprocessing Manager
    MANAGER = Manager()
    SHARED_LIST = MANAGER.list()  # List that will receive all results
    # List of regions to be scraped
    country_list = region_extractor(config.START_PAGE)
    # For each region creates a new process
    pool = Pool(processes=len(country_list))
    pool.map(activities_funnel, country_list)
    pool.close()
    csv_merger()
