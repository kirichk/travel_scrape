"""Config file for main.py
Contains settings like XPATHs, Selectors, Classes, etc."""

import requests
from selenium.webdriver.chrome.options import Options

# SETTINGS
START_URL = 'https://iwilltravelagain.com/'
START_PAGE = requests.get(START_URL)
CHROME_DRIVER_PATH = "C:/Users/NikolaiKyrychenko/Downloads/JUCE/chromedriver_win32/chromedriver.exe"
TIME_DELAY = 3 # Time difference between two pages in one process

# XPATH Values
XPATH_PAGINATION = '/html/body/main/section[3]/div[2]/div[4]/button[2]'
XPATH_NEXT_PAGE = '/html/body/main/section[3]/div[2]/div[4]/button[8]'

# Class Values
REGION_DIV_CLASS = 'block link-list text-left'
REGION_LI_CLASS = 'link-list-item'
ACTIVITY_ARTICLE_CLASS = 'activity-single__inner activity-single--card'
LINK_BUTTON_CLASS = 'a-button'

# CSS Selector Values
TITLE_SELECTOR = '#content > section.row.activity-standard--header.-row--with-banner-offset.-has-bg.-bg--image.-bg--dark.valign-middle > div > div > div.block.activity-title.heading.prose > div > h1'
CATEGORY_SELECTOR = '#content > section.row.activity-standard--content.js-activity-content-row > div > div.activity-content.js-activity-content > div.block.activity-upsell.prose > div > ul > li:nth-child(1) > div.quick-details-content > span:nth-child(2)'
LOCATION1_SELECTOR = '#content > section.row.activity-standard--content.js-activity-content-row > div > div.activity-content.js-activity-content > div.block.activity-upsell.prose > div > ul > li:nth-child(2) > div.quick-details-content > span:nth-child(2)'
LOCATION2_SELECTOR = '#content > section.row.activity-standard--content.js-activity-content-row > div > div.activity-content.js-activity-content > div.block.activity-upsell.prose > div > ul > li:nth-child(2) > div.quick-details-content > span:nth-child(3)'
LINK_SELECTOR = '#content > section.row.activity-standard--content.js-activity-content-row > div > div.activity-sidebar-col > div > aside > div.block.activity-buttons > div:nth-child(2) > a'

#Option that allow to run without opening a Chrome window
chrome_options = Options()
chrome_options.add_argument("--headless")
