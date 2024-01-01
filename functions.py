import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from email_scraper import scrape_emails

def generate_headers():
    header = Headers()
    return header.generate()



def scrape_search_results(keyword,amount):

    headers = generate_headers()

    #https://www.bing.com/search?q=cat+health+write+for+us&qs=n&sp=-1&lq=0&pq=cat+health+write+for+us&sc=11-23&sk=&cvid=6FCCD7C9B6B94A61A7A0E8684D026108&ghsh=0&ghacc=0&ghpl=&FPIG=BBA1A09D897248F09380525FF21642E0&first=21&FORM=PERE

    return #list of urls of pages





def scrape_email_from_source(url):

    headers = generate_headers()

    req = requests.get(url,headers=headers)

    soup = BeautifulSoup(req.content,'lxml')

    sc_email = scrape_emails(str(soup))

    searched_email = None

    if len(list(sc_email)) != 0 and list(sc_email)[0] != 'email@example.com':
        searched_email = list(sc_email)[0]

    
    return searched_email



def add_matrix(domain_list_with_email):
    return #return list of domains with dictionary email,matrix


