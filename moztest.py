import requests
from bs4 import BeautifulSoup


def get_da_pa_backlink(website):
    try:

        cookies = {
            'PHPSESSID': 'dm11v5867qp71p92ietuie31tm',
            'IR_gbd': 'thehoth.com',
            'IR_17808': '1704201577803%7C0%7C1704201577803%7C%7C',
            '_gcl_au': '1.1.1316895063.1704201579',
            '_ga_QGBHD36014': 'GS1.1.1704201579.1.0.1704201579.60.0.0',
            '_ga': 'GA1.2.754414552.1704201580',
            '_gid': 'GA1.2.693202146.1704201580',
            '_seg_uid_13478': '01HK558VB49JF938HSYG32MJ57',
            '_seg_uid': '01HK558VB49JF938HSYG32MJ57',
            '_seg_visitor_13478': 'eyJyZWZlcnJlciI6Imdvb2dsZS5jb20ifQ==',
            '_fbp': 'fb.1.1704201580411.1888896910',
            '_hjFirstSeen': '1',
            '_hjIncludedInSessionSample_957656': '1',
            '_hjSession_957656': 'eyJpZCI6ImIzMTRiMzJjLTE5ODAtNDEwZC1hOWMwLWViMDRhZTQ4ZTY0ZiIsImMiOjE3MDQyMDE1ODA1MjQsInMiOjEsInIiOjAsInNiIjoxfQ==',
            '_hjSessionUser_957656': 'eyJpZCI6IjU5YWIyN2M0LTg4NmYtNWY1Mi05ZDMzLWNjOTFkMTFkYWJhNyIsImNyZWF0ZWQiOjE3MDQyMDE1ODA1MTgsImV4aXN0aW5nIjp0cnVlfQ==',
            '_hjAbsoluteSessionInProgress': '1',
            '_tt_enable_cookie': '1',
            '_ttp': 'AyvGCJhEALcjsRT2Xvmbwh_mczG',
        }

        headers = {
            'authority': 'tools.thehoth.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            # 'cookie': 'PHPSESSID=dm11v5867qp71p92ietuie31tm; IR_gbd=thehoth.com; IR_17808=1704201577803%7C0%7C1704201577803%7C%7C; _gcl_au=1.1.1316895063.1704201579; _ga_QGBHD36014=GS1.1.1704201579.1.0.1704201579.60.0.0; _ga=GA1.2.754414552.1704201580; _gid=GA1.2.693202146.1704201580; _seg_uid_13478=01HK558VB49JF938HSYG32MJ57; _seg_uid=01HK558VB49JF938HSYG32MJ57; _seg_visitor_13478=eyJyZWZlcnJlciI6Imdvb2dsZS5jb20ifQ==; _fbp=fb.1.1704201580411.1888896910; _hjFirstSeen=1; _hjIncludedInSessionSample_957656=1; _hjSession_957656=eyJpZCI6ImIzMTRiMzJjLTE5ODAtNDEwZC1hOWMwLWViMDRhZTQ4ZTY0ZiIsImMiOjE3MDQyMDE1ODA1MjQsInMiOjEsInIiOjAsInNiIjoxfQ==; _hjSessionUser_957656=eyJpZCI6IjU5YWIyN2M0LTg4NmYtNWY1Mi05ZDMzLWNjOTFkMTFkYWJhNyIsImNyZWF0ZWQiOjE3MDQyMDE1ODA1MTgsImV4aXN0aW5nIjp0cnVlfQ==; _hjAbsoluteSessionInProgress=1; _tt_enable_cookie=1; _ttp=AyvGCJhEALcjsRT2Xvmbwh_mczG',
            'origin': 'https://tools.thehoth.com',
            'referer': 'https://tools.thehoth.com/tool/MozMetrics/run',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        data = {
            'targeturl': str(website),
        }

        response = requests.post('https://tools.thehoth.com/tool/MozMetrics/run', cookies=cookies, headers=headers, data=data)
        return response.content
    except:
        return None

def extract_td_elements(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all <td> elements in the parsed HTML
    td_elements = soup.find_all('td')
    
    # Initialize a list to store the text content of 2nd, 3rd, and 5th <td> elements
    extracted_data = []
    
    # Extract text content of the 2nd, 3rd, and 5th <td> elements (indices 1, 2, and 4)
    for index in [1, 2, 4]:
        if index < len(td_elements):
            extracted_data.append(td_elements[index].text.split("/")[0].strip())

    if len(extracted_data) == 0:
        return None
    
    return extracted_data


print(extract_td_elements(get_da_pa_backlink("https://platisoft.com")))