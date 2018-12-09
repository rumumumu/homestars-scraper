import requests
from bs4 import BeautifulSoup as bs
import json
from pprint import pprint
import re

#def = declare a function, we are declaring we want to scrape page 1?
# scrape_page(page=1) is a function that receive page as the argument
# the argument is optional, if its not found, the default is 1
# let me show you an example
def scrape_page(page=1):
    try:
        r = requests.get('https://homestars.com/on/toronto/architects?page=' + str(page))  # {} is used for dictionary, [] is used for list and () for function 
    except:
        return []
    #pprint(r.text) #only for debugging  r = results
    bs_ = bs(r.text, 'html.parser') #(creates beautifulsoup parser, to load the html text so we can manipulate it)
    return bs_.find_all('div', {'data-react-class' : 'SearchResult'}) #'' + "" = same in python

def get_links_from_scraped_page(result):
    urls = [] # initialized url as an empty list
    for x in result:
        data = json.loads(x['data-react-props']) # ( pull data from the json in divs named data-react-props? )(from the data-react-props value in div)
        try:
            urls.append(data['company']['url']) #try and look for 'company' and 'url', but if they don't exist just skip them
        except:
            #url is not found for that company
            continue

    return urls #return the urls that the function in try block searched for

def visit_company(url): #try and visit the url we scraped ( thi
    try:
        r = requests.get(url)
    except:
        return ''

    return r.text

def try_find_contact_us_link(html_page): #find a link that contain "contact" in its text
    bs_ = bs(html_page, 'html.parser') #run beautiful soup html parser
    url_elements = bs_.find_all('a') # 'a' is html element for link <a href='http://something.com'> a=anchor
    for elem in url_elements: # iterate all links
        try: # there are some broken links (doesnt have href)
            if elem['href'].lower().find('contact') != -1: #find if the link contain the word 'contact', lower() to convert to lower case
                return elem['href'] # return the link
        except:
            #do nothing
            pass #pass will do nothing, if we have other instruction below, it will continue. Return will break the loop.


def get_email_from_html(html_page): # get email from the company/contact page
    result = re.search(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z\.0-9]+)', html_page) #the r"..." something is another language by itself called regex
    if result is not None: # if it found a matching string (email)
        return result.groups()[0] # return the email
    return ''


#data = scrape_page() #execute the function scrape_page, put the result in our new data variable and "()" executes the function scrape_page
#print(get_links_from_scraped_page(data)) #(prints the links from the scraped page, data is passed to the function as argument "result", now result=data)

page_count = input('How many pages?') #ask the number of page, input 1 if you want to scrape 1 page(s)
emails = []
for i in range(1, int(page_count)+1): # iterate from page 1 to page_count (+1 is because range will generate 1..page_count-1) how about all of the pages?
    data = scrape_page(i) # call the function scrape_page
    urls = get_links_from_scraped_page(data) # get links from the page
    for url in urls: # iterate through all links
        html_page = visit_company(url) # try to visit the link
        email = get_email_from_html(html_page) # get the email
        if email == '': # if the email is not found on the home page
            contact_url = try_find_contact_us_link(html_page) #try and get the link to contact page
            if contact_url is not None: # if we found the contact page link
                html_page = visit_company(contact_url) # visit that
                email = get_email_from_html(html_page) # get the email from that page

        if email != '': # if we get an email after those 2 try
            emails.append(email) #add it to list
            print(email) # print it
    with open('result.txt', 'w') as f:  #instead of saving per email found, we will save per page scraped this line is equal with
                                        #f = open('result.txt', 'w') . . . close(f) "open result.txt in write mode, do some stuff, close the file
                                       
        f.write('\n'.join(set(emails))) # write a list of email separated by ENTER ('\n') .join will combine the list into string
#<-- example of .join -->
#wee = ['some', 'list', 'here']
#''.join(wee)
#'somelisthere'
#'\n'.join(wee)
#'some\nlist\nhere'
#</-- example over --/>
        
# set (some_list) will remove duplicate

print("FINISHED!")


