import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic,QtNetwork
from PyQt5.QtCore import *
from PyQt5.QtGui import QMovie, QPixmap,QDesktopServices
import requests
import re
import time
from functions import generate_headers
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from email_scraper import scrape_emails
import tldextract
import csv
import random
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class UI(QMainWindow):
	def __init__(self):
		super().__init__()
		uic.loadUi('ui/main.ui',self)
		self.mass_email_window = uic.loadUi('ui/send_email_form.ui')
		self.percentage = self.mass_email_window.findChild(QLabel,'percentage')

		self.percentage.hide()

		self.upload_btn = self.mass_email_window.findChild(QPushButton,'upload_btn')
		self.upload_btn.clicked.connect(self.upload_email_list)
		self.keyword = self.findChild(QTextEdit,"input_keyword")
		self.quant = self.findChild(QTextEdit,"input_quant")
		self.find_guest_post = self.findChild(QPushButton,"search_btn")
		self.find_guest_post.clicked.connect(self.find_guest_post_action)
		self.table = self.findChild(QTableWidget,"table")
		self.mass_email_window_opener_btn = self.findChild(QPushButton,"send_mass_email_open_btn")
		self.mass_email_window_opener_btn.clicked.connect(self.open_mass_email_window)
		self.add_email_window_opener_btn = self.findChild(QPushButton,"add_email_account_window_opener_btn")

		self.qemaillist = self.mass_email_window.findChild(QListWidget,"listWidget")

		self.add_email_window_opener_btn.clicked.connect(self.open_email_form)
		self.error = uic.loadUi('ui/error.ui')
		self.savedbtn = uic.loadUi('ui/saved.ui')
		self.email_form = uic.loadUi('ui/email_input_form.ui')

		self.email_input = self.email_form.findChild(QPlainTextEdit,'email_input')
		self.password_input = self.email_form.findChild(QPlainTextEdit,'password_input')
		self.email_submit_btn = self.email_form.findChild(QPushButton,'save_email')

		self.email_submit_btn.clicked.connect(self.add_email_account)

		self.email_list = []

		self.set_table_headers(self.table,["Domain", "Email", "DA", "PA", "Spam Score"])

		self.loading_label = self.findChild(QLabel,"loading_label")

		self.loading_bar = QMovie("static/progress_bar_loading.gif")
		self.loading_label.setMovie(self.loading_bar)
		self.loading_bar.start()

		self.loading_label.hide()

		self.download_label = self.findChild(QLabel,"download_img")
		

		

		self.download_btn = QMovie("static/download_img.gif")
		self.download_label.setMovie(self.download_btn)
		self.download_btn.start()

		self.download_label.installEventFilter(self)
		self.download_label.hide()

		self.email_subject_field=self.mass_email_window.findChild(QPlainTextEdit,"emailsubject")

		self.email_body_field=self.mass_email_window.findChild(QPlainTextEdit,"emailbody")

		self.email_send_mail_button=self.mass_email_window.findChild(QPushButton,"send_mail_button")

		self.email_send_mail_button.clicked.connect(self.send_mail_now)

		self.email_sent_ui = uic.loadUi('ui/email_sent.ui')




		#self.download_btn.clicked.connect(self.download)

		#self.loading_label.hide()

	#save button actions here.........
	def eventFilter(self, obj, event):
		if obj == self.download_label and event.type() == 2:
			#open save dialouge and save the csv file
			
			self.download()
            # Implement your desired action here
			return True
		return super().eventFilter(obj, event)
	
	def send_mail_now(self):
		if len(self.email_list) == 0 or len(self.email_subject_field.toPlainText()) == 0 or len(self.email_body_field.toPlainText())==0:
			self.error.show()
			return
		

		acc= open('email_account.txt','r')
		content = acc.read()
	
		email = str(content).split("+")[0]
		password = str(content).split("+")[1]

		acc.close()

		print(email,"  ",password)



		subject_field = self.email_subject_field.toPlainText()
		body_field = self.email_body_field.toPlainText()


		self.percentage.show()
		self.percentage.setText("      0 %")
		self.thread = EmailWorker(email,password,subject_field,body_field,self.email_list)
		self.thread.finished_signal.connect(self.email_proccess_done)
		self.thread.update_signal.connect(self.update_email)
		
		self.thread.start()

	def update_email(self,data):

		text_setup = round(data,2)
		
		self.percentage.setText(str(      text_setup)+"  %")

	def email_proccess_done(self):
		self.percentage.hide()
		self.email_sent_ui.show()

	
	def upload_email_list(self):
		

		filepath = self.open_file_dialogue_for_upload()

		email_list = self.get_emails(filepath)

		self.email_list = []

		self.email_list = email_list

		self.qemaillist.clear()

		

		self.mass_email_window.activateWindow()

		for email in self.email_list:
			self.qemaillist.addItem(email)


		print(filepath)
	
	def add_email_account(self):
		input_email = self.email_input.toPlainText()
		input_pass = self.password_input.toPlainText()

		if len(input_email)==0 or len(input_pass) == 0:
			self.error.show()

		else:
			fo = open("email_account.txt","w")
			fo.write(str(input_email)+"+"+str(input_pass))
			fo.close()

			if fo:
				self.savedbtn.show()
			else:
				self.error.show()
	
	def open_email_form(self):
		self.email_form.show()
	
	def save_table_to_csv(self,table_widget, file_path):
		try:
			with open(file_path, 'w', newline='') as csvfile:
				csv_writer = csv.writer(csvfile)
				
				# Write headers (column names)
				headers = []
				for column in range(table_widget.columnCount()):
					headers.append(table_widget.horizontalHeaderItem(column).text())
				csv_writer.writerow(headers)
				
				# Write data
				for row in range(table_widget.rowCount()):
					row_data = []
					for column in range(table_widget.columnCount()):
						item = table_widget.item(row, column)
						if item is not None:
							row_data.append(item.text())
						else:
							row_data.append('')
					csv_writer.writerow(row_data)
			
			print(f"Table data saved successfully to {file_path}")
			return True
		except Exception as e:
			print(f"Error saving table data: {e}")
			return False



	def download(self):
		file_path=self.open_file_dialouge()
		savefile = self.save_table_to_csv(self.table,file_path)

		if savefile == True:
			self.savedbtn.show()
			self.download_label.hide()
			print("hello saved")

		else:
			print("error saving file")

	def get_emails(self,file_path):

		df = pd.read_csv(file_path)

		emails = list(set(list(df["Email"])))

		for email in emails:
			if email == None or email == "" or email == " " or len(email.split(" ")) > 1 or "example" in email:
				del emails[emails.index(email)]



		return emails


	def open_file_dialogue_for_upload(self):
		options = QFileDialog.Options()
		# Set the file dialog to open mode
		file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Csv Files (*.csv);;All Files (*)", options=options)
		
		if file_name:
			# Do something with the selected file path (e.g., read the file)
			print(f"Selected file path: {file_name}")
			# Implement your file reading logic here

			return file_name


		else:
			return None


	def open_file_dialouge(self):
		options = QFileDialog.Options()
        # Set the file dialog to save mode
		file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Csv Files (*.csv);;All Files (*)", options=options)
		if file_name:
            # Do something with the selected file path (e.g., save a file)
			print(f"Selected file path: {file_name}")
            # Implement your file saving logic here

			return file_name
		else:
			return None
	
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
		
		

		
		self.loading_label.show()
		self.thread = Worker(keyword,site_amount)
		self.thread.finished_signal.connect(self.proccess_done)
		self.thread.update_signal.connect(self.update_status)
		self.find_guest_post.hide()
		self.thread.start()
		



	def update_status(self,data):
		
		self.insert_data_into_table(self.table,data)


	def proccess_done(self):
		print("done")
		self.find_guest_post.show()
		self.loading_label.hide()
		self.download_label.show()

		
	
	
	
	def set_table_headers(self,table,headers):

		table.setColumnCount(len(headers))
		table.setHorizontalHeaderLabels(headers)
		total_width = table.viewport().size().width()
		for col, percentage in enumerate([35,35,5,5,15]):
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

	def get_da_pa(self,domain):

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
						try:
							mozdata = self.get_da_pa(check_this_link_domain)
							da = mozdata[0]
							pa = mozdata[1]
							spam_score = mozdata[2]

						except:
							da = 0
							pa = 0
							spam_score = 0

						new_data = {"url":check_this_link_domain,"email":found_email,"DA":da,"PA":pa,"Spam_score":spam_score}
						self.update_signal.emit(new_data)
				except:
					print("something went wrong... next")
					

			#now add DA PA Spam scroe matrix to a new dictionary with prvious data, like this - [{"url":"test.com","email":"test@gmail.com","DA":34,"PA":11,"spam_score":13}]

			#next update the table adding these new rows on the GUI table . emit the update
			print("done task...")

		self.finished_signal.emit(1)



class EmailWorker(QThread):
	def __init__(self,email,password,subject,body,email_list):
		self.email = email
		self.password = password
		self.email_list = email_list
		self.subject = subject
		self.body = body
		super().__init__()

	finished_signal = pyqtSignal(int)
	update_signal = pyqtSignal(float)



	def send_email(self,gmail_username, app_password, subject, body, to_email):
		# Set up the email parameters
		sender_email = gmail_username
		recipient_email = to_email

		message = MIMEMultipart()
		message['From'] = sender_email
		message['To'] = recipient_email
		message['Subject'] = subject

		# Add the email body to the message
		message.attach(MIMEText(body, 'plain'))

		# Create a secure SSL context
		context = smtplib.SMTP_SSL('smtp.gmail.com', 465)

		try:
			# Login to the Gmail account
			context.login(sender_email, app_password)

			# Send the email
			context.sendmail(sender_email, recipient_email, message.as_string())
			print(f"Email successfully sent to {recipient_email}")

		except Exception as e:
			print(f"An error occurred while sending the email: {e}")

		finally:
			# Close the connection
			context.quit()


	def run(self):
			
			i=1
			
			for email in self.email_list:
				try:
					self.send_email(self.email,self.password,self.subject,self.body,email)
					cal_percentage = (i/len(self.email_list))*100
					self.update_signal.emit(round(cal_percentage,2))

				except:
					print("can not send email")

				i+=1

			self.finished_signal.emit(1)
					








			

		
		#end the loop and emit the finished

			
				





		
		

    

app = QApplication(sys.argv)

ui = UI()
ui.show()

sys.exit(app.exec_())
		