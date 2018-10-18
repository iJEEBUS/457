#!/usr/bin/env python
"""
A script that scrapes, cleans, generates a CSV file, and transforms the restaurant
inspection data of Grand Rapids into a pandas dataframe.
"""
__author__ = 'Ronald Rounsifer'
__version__ = '7.10.2018'
__license__ = 'MIT License'

from selenium import webdriver
from bs4 import BeautifulSoup
import requests




# Get source code from website
__DATE = "2018-07-19"
__URL = "https://www.myfitnesspal.com/food/diary"
driver = webdriver.PhantomJS() # Driver to load the JS
driver.get(__URL)

element = WebDriverWait(driver, 10)


html = driver.execute_script("return document.documentElement.innerHTML")
soup = BeautifulSoup(html, "lxml")


print soup.find_all(class_="js-show-edit-food")
