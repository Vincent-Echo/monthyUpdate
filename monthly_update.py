import os
import re
from bs4 import BeautifulSoup

zebra = 'www.zebra.com'
os.system('wget www.zebra.com/us/en.html -O list.html')
soup = BeautifulSoup(open('list.html'))
#Get all printer list
printer_list = soup.find('select')
printers = {}

for child in printer_list.children:
	if (child != '\n'):
		if (child.string != u'Select Printer'):
			#html string are all in utf-8, so we need decode first.
			printer_url = 'www.zebra.com' + child['value'].encode("utf-8")
			#we need not others like network card.
			m = re.search('(desktop|mobile|industrial|passive-rfid|print-engine)', printer_url)
			if(m):
				#printer_url value can be 'http://www.zebra.com/us/en/support-downloads/print-engine/110xi4.html' 
				strs = re.split('/', printer_url)
				printer = re.sub('.html', '', strs[-1])
				printers[printer] = printer_url

#record driver and firmware version				
log_file = open('tmp.log', 'w')

#Driver name, version, download url info
def get_driver_info(driver_tr_tag):
	if (driver_tr_tag.contents[1].string):
		driver_name = driver_tr_tag.contents[1].string.encode("utf-8")
	else
		driver_name = "Zebra Setup Utilities"
	driver_version = driver_tr_tag.contents[3].string.encode("utf-8")
	driver_support_os = driver_tr_tag.contents[5].string.encode("utf-8")
	driver_download_link = "www.zebra.com" + driver_tr_tag.contents[7].a['href'].encode("utf-8")
	log_file.write(driver_name + '\n')
	log_file.write(driver_version + '\n')
	log_file.write(driver_support_os + '\n')
	#This function can get driver or firmware download url 
	get_driver_or_firmware_download_href(driver_download_link, 'drivers')


log_file.close()