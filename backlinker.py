import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic,QtNetwork
from PyQt5.QtCore import *
from PyQt5.QtGui import QMovie, QPixmap,QDesktopServices
import requests
import re
from functions import generate_headers
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from email_scraper import scrape_emails
import tldextract

class UI(QMainWindow):
	def __init__(self):
		super().__init__()
		uic.loadUi('ui/main.ui',self)
		self.mass_email_window = uic.loadUi('ui/send_email_form.ui')
		self.keyword = self.findChild(QTextEdit,"input_keyword")
		self.quant = self.findChild(QTextEdit,"input_quant")
		self.find_guest_post = self.findChild(QPushButton,"search_btn")
		self.find_guest_post.clicked.connect(self.find_guest_post_action)
		self.table = self.findChild(QTableWidget,"table")
		self.mass_email_window_opener_btn = self.findChild(QPushButton,"send_mass_email_open_btn")
		self.mass_email_window_opener_btn.clicked.connect(self.open_mass_email_window)
		self.add_email_window_opener_btn = self.findChild(QPushButton,"add_email_account_window_opener_btn")
		self.error = uic.loadUi('ui/error.ui')

		self.set_table_headers(self.table,["Domain", "Email", "DA", "PA", "Spam Score"])
		

	
	
	def open_mass_email_window(self):
		self.mass_email_window.open()


	def find_guest_post_action(self):
		keyword = self.keyword.toPlainText()
		site_amount = self.quant.toPlainText()

		if len(keyword) < 4:
			self.error.show()
			return
		
		else:
			keyword = keyword.strip()
		
		if len(site_amount) == 0:
			self.error.show()
			return
		

		try:
			site_amount = int(site_amount.strip())
		
		except:
			self.error.show()
			return
		
		

		

		self.thread = Worker(keyword,site_amount)
		self.thread.finished_signal.connect(self.proccess_done)
		self.thread.update_signal.connect(self.update_status)
		self.thread.start()
		



	def update_status(self,data):
		
		self.insert_data_into_table(self.table,data)


	def proccess_done(self):
		print("done")
		pass

		
	
	
	def set_table_headers(self,table,headers):

		table.setColumnCount(len(headers))
		table.setHorizontalHeaderLabels(headers)
		total_width = table.viewport().size().width()
		for col, percentage in enumerate([35,40,5,5,15]):
			size = int(total_width * (percentage / 100))
			table.setColumnWidth(col, size)

	def insert_data_into_table(self,table, data):
    # Insert a new row at the top
		table.insertRow(0)

    # Iterate over the dictionary and fill the table
		for col, key in enumerate(data.keys()):
			value = data.get(key, "")
			table.setItem(0, col, QTableWidgetItem(str(value)))
	

class Worker(QThread):
	def __init__(self,keyword,site_amount):
		self.keyword = keyword
		self.site_amount = site_amount
		super().__init__()

	finished_signal = pyqtSignal(int)
	update_signal = pyqtSignal(dict)

	def scrape_email_from_source(self,url):

		headers = generate_headers()
		try:
			req = requests.get(url,headers=headers)
		except:
			return None

		soup = BeautifulSoup(req.content,'lxml')

		sc_email = scrape_emails(str(soup))

		searched_email = None

		if len(list(sc_email)) != 0 and list(sc_email)[0] != 'email@example.com':
			searched_email = list(sc_email)[0]

		
		return searched_email


	def search_on_bing(self,query,pos=0):

		req_url = f"https://www.bing.com/search?q={query}+write+for+us&first={pos}"

		headers = generate_headers()

		try:

			res = requests.get(req_url)
			content = res.content

		except:
			content = None


		return content

	def extract_urls_from_html(self,html_content):
    # Parse the HTML content using BeautifulSoup
		soup = BeautifulSoup(html_content, 'html.parser')
		
		# Find all li elements with class 'b_algo'
		li_elements = soup.find_all('li', class_='b_algo')
		
		# List to store the href values
		href_list = []
		
		# Loop through each li element to find the 'a' tag and extract href
		for li in li_elements:
			# Find the 'a' element inside the li
			a_tag = li.find('a')
			
			# Check if the 'a' element exists and has href attribute
			if a_tag and 'href' in a_tag.attrs:
				href_list.append(a_tag['href'])
				
		return href_list

	def run(self):
		total_pages = int((int(self.site_amount)*4)/10)

		pos_tracking = 0

		url_list = []
		
		for pagenum in range(total_pages):
			#self.update_signal.emit({"domain":"https://facebook.com","email":"iamshakibulislam@gmail.com","DA":0,"PA":0,"Spam_score":10})
			#self.finished_signal.emit(1)
			print("loop starting - ",pagenum)
			

			if pos_tracking == 0:
				this_page_content = self.search_on_bing(self.keyword,pos_tracking)
				pos_tracking += 1
			else:
				pos_tracking += 10
				this_page_content = self.search_on_bing(self.keyword,pos_tracking)

			print(this_page_content)
			new_urls = self.extract_urls_from_html(this_page_content)

			url_list += new_urls

			print("new urls is : ",new_urls)

			#now extract email addresses from these urls and output in a dictionary with root domain

			for url in new_urls:
				print("url is - ",url)
				try:
					found_email=self.scrape_email_from_source(url)
					if found_email != None:
						get_root_domain = tldextract.extract(url)
						check_this_link_domain = 'https://'+get_root_domain.domain+'.'+get_root_domain.suffix
						new_data = {"url":check_this_link_domain,"email":found_email,"DA":0,"PA":0,"Spam_score":0}
						self.update_signal.emit(new_data)
				except:
					print("something went wrong... next")
					

			#now add DA PA Spam scroe matrix to a new dictionary with prvious data, like this - [{"url":"test.com","email":"test@gmail.com","DA":34,"PA":11,"spam_score":13}]

			#next update the table adding these new rows on the GUI table . emit the update
			print("done task...")
			break

		
		#end the loop and emit the finished

			
				





		
		

    

app = QApplication(sys.argv)

ui = UI()
ui.show()

sys.exit(app.exec_())
		