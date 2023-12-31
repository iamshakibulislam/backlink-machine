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



	def update_status(self):
		pass


	def proccess_done(self):
		pass

		


	

class Worker(QThread):
	def __init__(self,keyword,site_amount):
		self.keyword = keyword
		self.site_amount = site_amount

	finished_signal = pyqtSignal(int)
	update_signal = pyqtSignal(dict)

	def search_on_bing(query,pos=0):

		req_url = f"https://www.bing.com/search?q={query} +write+for+us&qs=n&sp=-1&lq=0&pq={query} +write+for+us&sc=11-23&sk=&cvid=6FCCD7C9B6B94A61A7A0E8684D026108&ghsh=0&ghacc=0&ghpl=&FPIG=BBA1A09D897248F09380525FF21642E0&first={pos}&FORM=PERE"

		headers = generate_headers()

		try:

			res = requests.get(req_url,headers=headers)
			content = res.content

		except:
			content = None


		return content

	def extract_urls_from_html(html_content):
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
		
		for pagenum in total_pages:

			if pos_tracking == 0:
				this_page_content = self.search_on_bing(self.keyword,pos_tracking)
				pos_tracking += 1
			else:
				pos_tracking += 10
				this_page_content = self.search_on_bing(self.keyword,pos_tracking)

			
			new_urls = self.extract_urls_from_html(this_page_content)

			url_list += new_urls

			#now extract email addresses from these urls and output in a dictionary with root domain

			#now add DA PA Spam scroe matrix to a new dictionary with prvious data, like this - [{"url":"test.com","email":"test@gmail.com","DA":34,"PA":11,"spam_score":13}]

			#next update the table adding these new rows on the GUI table . emit the update

		
		#end the loop and emit the finished

			
				





		
		

    

app = QApplication(sys.argv)

ui = UI()
ui.show()

sys.exit(app.exec_())
		