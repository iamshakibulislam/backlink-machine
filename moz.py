

from bs4 import BeautifulSoup
import requests

import random



def get_da_pa(domain):

	try:

		letter = "abcdefghijklmnopqrstuvwxyz"
		randstr=letter[random.randint(0,25)]+letter[random.randint(0,25)]



		
		cookies = {
	    '_ga': 'GA1.2.1854752040.1703849013',
	    '_gid': 'GA1.2.2133451622.1704200455',
	    'PHPSESSID': f'5a0bc61a1fdd307dcd0600ab3be7549{randstr}',
		}

		headers = {
		    'authority': 'www.robingupta.com',
		    'accept': '*/*',
		    'accept-language': 'en-US,en;q=0.9',
		    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
		    # 'cookie': '_ga=GA1.2.1854752040.1703849013; _gid=GA1.2.2133451622.1704200455; PHPSESSID=5a0bc61a1fdd307dcd0600ab3be7549fa',
		    'origin': 'https://www.robingupta.com',
		    'referer': 'https://www.robingupta.com/bulk-domain-authority-checker.html',
		    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
		    'sec-ch-ua-mobile': '?0',
		    'sec-ch-ua-platform': '"Windows"',
		    'sec-fetch-dest': 'empty',
		    'sec-fetch-mode': 'cors',
		    'sec-fetch-site': 'same-origin',
		    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
		    'x-requested-with': 'XMLHttpRequest',
		}

		data = {
		    'website_name': f'{domain}',
		    'da': 'y',
		    'pa': 'y',
		    'ss': 'y',
		    'page_token': 'get_website',
		    'mng_t': '0',
		    'mng_2_api_urls': 'https://thefashionhubs.com/wp-content/plugins/mng_bulk_domain_authority_api_v3/api.php',
		}

		response = requests.post(
		    'https://www.robingupta.com/wp-content/plugins/mng_domain_auth_v3//alexa.action.php',
		    cookies=cookies,
		    headers=headers,
		    data=data,
		)

		#finally get the da pa spam score

		cookies = {
	    '_ga': 'GA1.2.1854752040.1703849013',
	    '_gid': 'GA1.2.2133451622.1704200455',
	    'PHPSESSID': f'5a0bc61a1fdd307dcd0600ab3be7549{randstr}',
		}

		headers = {
		    'authority': 'www.robingupta.com',
		    'accept': '*/*',
		    'accept-language': 'en-US,en;q=0.9',
		    # 'cookie': '_ga=GA1.2.1854752040.1703849013; _gid=GA1.2.2133451622.1704200455; PHPSESSID=5a0bc61a1fdd307dcd0600ab3be7549fa',
		    'referer': 'https://www.robingupta.com/bulk-domain-authority-checker.html',
		    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
		    'sec-ch-ua-mobile': '?0',
		    'sec-ch-ua-platform': '"Windows"',
		    'sec-fetch-dest': 'empty',
		    'sec-fetch-mode': 'cors',
		    'sec-fetch-site': 'same-origin',
		    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
		    'x-requested-with': 'XMLHttpRequest',
		}

		response = requests.get(
		    f'https://www.robingupta.com/wp-content/plugins/mng_domain_auth_v3//alexa.action.php?sitename={domain}&page_token=get_website&null&da=y&pa=y&ss=y&v=1',
		    cookies=cookies,
		    headers=headers,
		)


		soup = BeautifulSoup(response.content,'html.parser')

		th_tags = soup.find_all('th')

		last_three_values = [th.text.strip() for th in th_tags[-3:]]



		return last_three_values

	except:
		return [0,0,0]




print(get_da_pa("https://platisoft.com"))