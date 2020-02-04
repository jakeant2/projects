from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import html_text
import pandas as pd
import time
from datetime import datetime

# twitter account search scraper

url = 'https://twitter.com/'
driver = webdriver.Firefox()
driver.set_window_position(0,0)
driver.set_window_size(950,800)
driver.get(url)
time.sleep(1.5)

credential1 = 'USERNAME'
credential2 = 'PASSWORD'
credential3 = 'ENTER SEARCH HERE'

login_button = driver.find_element_by_css_selector('a.css-1dbjc4n:nth-child(5)')
login_button.click()

username = driver.find_element_by_name('session[username_or_email]')
username.send_keys(credential1)

password = driver.find_element_by_name('session[password]')
password.send_keys(credential2)

login = driver.find_element_by_css_selector('div.css-18t94o4')
login.click()
time.sleep(2)

search = driver.find_element_by_css_selector('a.r-1habvwh:nth-child(2)')
search.click()
time.sleep(1)

search_input = driver.find_element_by_css_selector('.r-30o5oe')
search_input.send_keys(credential3)
time.sleep(.5)
search_input.send_keys(Keys.ENTER)
time.sleep(2)

view_accounts = driver.find_element_by_css_selector('div.r-tzz3ar:nth-child(2) > div:nth-child(3) > a:nth-child(1)')
view_accounts.click()

account_names = []
account_tags = []
account_link = []
account_bio = []

def scroll():

	SCROLL_PAUSE_TIME = 1
	global account_name

	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")
	while True:
	    # Scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		# Wait to load page		
		time.sleep(SCROLL_PAUSE_TIME)		
		account_name = driver.find_elements_by_xpath('//*[@id="react-root"]/div/div/div/main/div/div/div/div/div/div[2]/div/div/section/div/div/div/div/div/div/div/div[2]/div[1]/div[1]/a/div/div[1]/div[1]/span/span')
		for act_name in account_name:
			global acctname
			acctname = act_name.text
			account_names.append(acctname)

		account_handle = driver.find_elements_by_xpath('//*[@id="react-root"]/div/div/div/main/div/div/div/div/div/div[2]/div/div/section/div/div/div/div/div/div/div/div[2]/div[1]/div[1]/a/div/div[2]/div/span')
		for act_handle in account_handle:
			global account_tags
			acct_handles = act_handle.text
			account_tags.append(acct_handles)

		soup = BeautifulSoup(driver.page_source, 'lxml')
		account_links = soup.find_all('a', href=True, class_='css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l')
		for acct_links in account_links:
			global act_link
			act_link = acct_links['href']
			account_link.append(act_link)


		# Calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height

scroll()


print('\n')
print('# of Accounts', len(account_names))
print('\n')
print('Account Names: ', account_names)
print('\n')
print('Account Handles: ', account_tags)
print('\n')
print('Account Links: ', account_link)
print('\n')

driver.close()

print("Beginning to extract data to xlsx File: ")
print("\n")

# creating and formatting csv
xlName = credential3 + '_twitter_pages' + '.xlsx'
# create pandas dataframe to create properly structured csv file with headers
df = pd.DataFrame({'Account Name':account_names})
df1 = pd.DataFrame({'Account Handle':account_tags})
df2 = pd.DataFrame({'Link':account_link})
final = pd.concat([df, df1, df2], axis=1)

final.to_excel(xlName, index=False)
print(final)
