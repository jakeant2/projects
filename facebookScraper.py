from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import html_text
import pandas as pd
import time
from datetime import datetime


# parsing facebook search

driver = webdriver.Firefox()
driver.get('https://www.facebook.com/')
time.sleep(1)

# username
credential1 = 'EMAIL'
# password
credential2 = 'PASSWORD'
# search
credential3 = 'WHAT YOU WANT TO SEARCH'
#finding username text field
email = driver.find_element_by_xpath('//*[@id="email"]')
#entering username
email.send_keys(credential1)
#finding password text field
password = driver.find_element_by_xpath('//*[@id="pass"]')
#entering password
password.send_keys(credential2)
time.sleep(1)
#find login button
signin = driver.find_element_by_xpath('//*[@id="loginbutton"]')
# pretty self explanitory
signin.click()
# giving it time to load
time.sleep(2)
# finding search bar 
findSearch = driver.find_element_by_name('q')
# entering search
search = findSearch.send_keys(credential3)
# telling selenium to press enter to search rather than clicking search button
findSearch.send_keys(Keys.RETURN)
# waiting to load
time.sleep(1)
# changing search to only get pages results
searchPages = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div/div/div/div/div/div/ul/li[7]/a')
searchPages.click()
time.sleep(3)


def scroll():

	SCROLL_PAUSE_TIME = 1

	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")
	while True:
	    # Scroll down to bottom
	    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	    # Wait to load page
	    time.sleep(SCROLL_PAUSE_TIME)
	    # Calculate new scroll height and compare with last scroll height
	    new_height = driver.execute_script("return document.body.scrollHeight")
	    if new_height == last_height:
	        break
	    last_height = new_height
scroll()

datalist = []
linklist = []
soup = BeautifulSoup(driver.page_source, 'lxml')
#finding # of results
number = soup.find_all('div', class_='_glj')
# names of pages
for pageName in number:
	names = pageName.find_all('span', string=True)
	name = html_text.extract_text(str(names))
	datalist.append(name)

pagelink = soup.find_all(class_='_32mo', href=True)
for link in pagelink:
	pageLink = link['href']
	pagelink = [pageLink]
	linklist.append(pagelink)

driver.close()


print('\n')
print(' # of pages: ', len(number))
print('\n')
print('Page Names: ', datalist)
print('\n')
print('Page Links: ', linklist)
print('\n')


# create date and time stamp for the excel filename format: drexel_collegeName_MMDDYYYY-HHMMSS.csv

print("Beginning to extract data to xlsx File: ")
print("\n")

# creating and formatting csv
xlName = 'SEARCH_FBpages' + '.xlsx'
# create pandas dataframe to create properly structured csv file with headers
df = pd.DataFrame({'Page Name':datalist, 'Link':linklist})
df.to_excel(xlName, index=False)
