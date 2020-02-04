# projects
An assortment of python projects i have completed, have been using python for about two and a half weeks as of first file posting in 1/2020.


facebook scraper was completed to log into facebook, and search for pages about a custom search. 
    to use you will need to install required libraries(selenium, bs4, pandas), then insert your email, password, and what you want to search in the corresponding credential variables.
    it will scroll all the way to the bottom of your search, if it operates correctly. 

twitter scraper was used for the exact same thing, just on twitter
    uses a scroll loop as well to gather required elements as it goes, as the html will only show you the accounts that are in      the current window rather than a total of them all when you attempt to scrape all at once. 
    same libraries must be installed, and username, password along with your search input must be customized. 
    window height must stay the same; the html will vary if you change window size and you will need to edit all desired elements again.
