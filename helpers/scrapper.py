# -*- coding: utf-8 -*-
"""
__author__ = "Ashiquzzaman Khan"
__desc__ = "scraper helper file"
"""
import os
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from helpers.generic_helpers import EXCEPTION_KEYWORD

__all__ = [
    'login',
    'close',
    'get_driver',
    'get_likers',
    'get_profile_like',
    'get_commenters'
]

LOGIN_URL = "https://m.facebook.com/"

def get_driver(_os):
    """
    functions to get the driver with options
    :param _os: string name of the operating system
    :param _browser: string name of the browser
    :return: the web driver object with customized options
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['acceptSslCerts'] = True
    capabilities['acceptInsecureCerts'] = True
    if _os == "mac":
        _executable = os.path.abspath('./Binary/mac/chromedriver')
    elif _os == "windows":
        _executable = os.path.abspath('./Binary/windows/chromedriver.exe')
    elif _os == "linux":
        _executable = os.path.abspath('./Binary/linux/chromedriver')

    return webdriver.Chrome(chrome_options=options, executable_path=_executable, desired_capabilities=capabilities)

def close(_driver):
    """
    functions for closing the web driver
    :param _driver: the web driver object
    :return:
    """
    _driver.close()             # closing the driver


def more_locator(_driver):
    """
    functions for locating See more button
    :param _driver: web driver object
    :return: the See more button or None
    """
    try:
        return _driver.find_element_by_xpath("//*[contains(text(), 'See more…')]")
    except NoSuchElementException:
        return None


def get_view_previous_locator(_driver):
    """
    functions for locating view previous comments button
    :param _driver: web driver object
    :return: the View Previous Button or None
    """
    try:
        return _driver.find_element_by_xpath("[//*contains(text(), 'View previous comments…')]") # click on the all likes button
    except NoSuchElementException:
        return None


def fast_scroll(_driver, _timeout, _element="document.body"):
    """
    functions for scrolling the page fast
    :param _driver: web driver object
    :param _element: the element which needs to be scrolled in body
    :return:
    """
    time.sleep(_timeout)
    last_height = _driver.execute_script(f"return {_element}.scrollHeight")     # Get scroll height
    while True:
        time.sleep(_timeout)
        _driver.execute_script(f"window.scrollTo(0, {_element}.scrollHeight);")  # Scroll down to bottom
        time.sleep(_timeout)  # Wait to load page
        # Calculate new scroll height and compare with last scroll height
        new_height = _driver.execute_script(f"return {_element}.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    time.sleep(_timeout)


def login(_driver, _timeout, _username, _password):
    """
    functions for login to facebook
    :param _driver: the web driver object
    :param _username: a string provided by the flask input
    :param _password: a string provided by the flask input
    :return:
    """
    _driver.get(LOGIN_URL)                                  # get the login page
    time.sleep(_timeout)                                         # wait for the page to load
    username = _driver.find_element_by_id("m_login_email")  # find the username input
    username.send_keys(_username)                           # pass the username
    password = _driver.find_element_by_name("pass")
    # password = _driver.find_element_by_id("m_login_password")# find the password input
    password.send_keys(_password)                           # pass the password
    password.send_keys(Keys.RETURN)                         # simulate enter / return key of keyboard
    time.sleep(_timeout)                                         # wait for the next page to load


def get_likers(_driver, _timeout):
    """
    functions for getting the likers of a post
    :param _driver: web driver object
    :return: two list
    """
    _likers_name_list = []                                      # the first list of names that will be returned
    _likers_profile_list = []                                   # the second list of profile links that will be returned
    _driver.find_element_by_class_name("_1g06").click()         # click on the all likes button
    time.sleep(_timeout)                                             # wait for the pages to load
    more = more_locator(_driver)                                # find the see more button
    while more != None:
        more.click()                                            # click on more buttons
        time.sleep(_timeout)                                         # wait to load more
        more = more_locator(_driver)                            # find again the more button

    html_doc = _driver.page_source                              # dumping the page for scrapping data
    soup = BeautifulSoup(html_doc, 'lxml')                      # making soup for navigating through HTML
    block = soup.findAll("div", {'class': '_4mn'})              # isolate all likers name and profile_link div

    for b in block:
        profile_link = b.find("a")['href']                      # finding the profile link
        full_profile_link = LOGIN_URL + profile_link            # post process to absolute url
        _likers_profile_list.append(full_profile_link)          # adding the URL to the list

        name = b.find("strong").text                            # finding the name
        for i in EXCEPTION_KEYWORD:
            if i in name:
                name = name.replace(i, "")                      # replace any dot in names because mongo doesn't allow dot

        _likers_name_list.append(name)                          # adding the name to the list

    return _likers_name_list, _likers_profile_list              # return the two list


def get_commenters(_driver, _timeout):
    """
    functions to get commenters
    :param _driver: webd river object
    :return: two list
    """
    _commenters_name_list = []                                      # the first list of names that will be returned
    _commenters_profile_list = []                                   # the second list of profile links that will be returned

    view_previous_button = get_view_previous_locator(_driver)       # get previous button

    while view_previous_button != None:
        view_previous_button.find_element_by_xpath("..").click()    # previous button click
        time.sleep(_timeout)                                             # wait for page to load
        view_previous_button = get_view_previous_locator(_driver)   # get previous button again

    html_doc = _driver.page_source                                  # dump the html of pages
    soup3 = BeautifulSoup(html_doc, 'lxml')                         # make beautiful soup

    all_blocks = soup3.findAll('div', {'class':'_2b05'})            # get the blocks that holds data
    for blocks in all_blocks:
        profile_link = blocks.find("a")['href']                     # get profile links of the commenters
        absolute_profile_link = LOGIN_URL + profile_link            # make the links absolute
        _commenters_profile_list.append(absolute_profile_link)      # append to list

        name = blocks.find("a").text                                # get the name of the commenters
        for i in EXCEPTION_KEYWORD:
            if i in name:
                name = name.replace(i, "")                          # replace any dot in names because mongo doesnt allow dot

        _commenters_name_list.append(name)                          # append to the list

    return _commenters_name_list, _commenters_profile_list          # return the two list


def get_profile_like(_driver, _timeout, _likes_dict, _current_name, _url):
    """
    functions to get all likes from a profile
    :param _driver: the web driver
    :param _list: list of names
    :param _url_list: list of urls
    :return: dictionary with names and their likes
    """
    _profile_likes_link = {}  # the dictionary that will be returned
    _driver.get(_url)# load the profile
    time.sleep(_timeout)  # wait to load the page
    # check if the profile is a page or not
    try:
        _flags = _driver.find_element_by_xpath("//*[contains(text(), 'Reviews')]")  # its a page
    except NoSuchElementException:
        _flags = None  # Its not a page

    if _flags == None:
        _about_page = WebDriverWait(_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'About')]")))  # locate the about page
        _about_page.click()  # clicking the about page
        fast_scroll(_driver=_driver, _timeout=_timeout)  # scroll to reveal likes

        time.sleep(_timeout)  # wait to load the pages
        try:
            _likes = _driver.find_element_by_xpath("//*[contains(text(), 'Likes')]")
        except NoSuchElementException or TimeoutException:
            _likes = None

        if _likes != None:
            _likes.find_element_by_xpath("../../..").click()  # locate the parent button to click
            time.sleep(_timeout)  # wait for the page to load

            _all_likes = WebDriverWait(_driver, _timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'All Likes')]")))  # locate the all likes
            _all_likes.find_element_by_xpath("../../../..").click()  # get the all likes parents and click
            time.sleep(_timeout)  # wait for the page to load
            fast_scroll(_driver=_driver, _timeout=_timeout)  # scroll to reveal more
            time.sleep(_timeout)  # wait to load the page
            html_doc_likes = _driver.page_source  # dump the page
            soup2 = BeautifulSoup(html_doc_likes, 'lxml')  # make soup to navigate the html
            b = soup2.findAll('div', {'class': '_1a5p'})  # get all the liked item

            for j in b:
                _liked_item_text = j.find('div', {'class': '_1a5r'}).find('span').text  # get the text

                for k in EXCEPTION_KEYWORD:
                    if k in _liked_item_text:
                        _liked_item_text = _liked_item_text.replace(k, "")

                _link = j.find('a')['href']
                _link_processed = "https://www.facebook.com" + _link
                _profile_likes_link[_liked_item_text] = _link_processed
            _likes_dict[_current_name] = _profile_likes_link  # put it on dictionary

        else:
            _likes_dict[_current_name] = {
                'Empty or Restricted': "Empty or Restricted"}  # put it on dictionary in case not found
    time.sleep(_timeout)                                                     # wait one seconds