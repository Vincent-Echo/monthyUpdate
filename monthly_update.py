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

#Get download url of the driver or firmware
def get_driver_or_firmware_download_href(href, type):
	m = re.search(ur'(-.*)\&c=us\&l=en', href)
	href = 'http://www.zebra.com/us/en/support-download/eula.' + m.group(1)[0] + '.html'
	os.system('wget "' + href + '" -O driver_temp.html')
	soup = BeautifulSoup(open('driver_temp.html'))
	tag_a_s = soup.findAll('a', sctype = type)
	down_href = zebra + tag_a_s[0]['href'].encode("utf-8")
	log_file.write(down_href + '\n')


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


#Firmware name, version , download url info
def get_firmware_info(fw_tr_tag):
		fw_ver = ''
		fw_rea_note = ''
		fw_desc = ''
		fw_ver = fw_tr_tag.contents[1].string.encode("utf-8")
		if (fw_tr_tag.contents[3].string):
			fw_rea_note = fw_tr_tag.contents[3].string.encode("utf-8")
		if (fw_tr_tag.contents[5].string)
			fw_desc = fw_tr_tag.contents[5].string.encode("utf-8")
			
		fw_donwload_link = "www.zebra.com" + fw_tr_tag.contents[7].a['href'].encode("utf-8")
		log_file.write(fw_ver + '\n')
		log_file.write(fw_rea_note + '\n')
		log_file.write(fw_desc + '\n')
		#This function can get driver or firmware download url 
		get_driver_or_firmware_download_href(fw_donwload_link, 'firmware')

#Get driver tag and firmware tag from main page of the printer		
def get_driver_and_firmware_info(printer, url):
	os.system('wget ' + url + ' -O' + printer + '.html')
	soup = BeautifulSoup(open(printer + '.html'))
	driver_part = soup.findAll('div', attrs = {"class": "tab-content filterable",
												"data-tab-label": "Drivers",
												"data-tab-id": "drivers"})
	firmware_part = soup.findAll('div', attrs = {"class": "tab-content filterable",
												 "data-tab-label": "Firmware & Service Packs",
												 "data-tab-id": "fimware-servicepacks"})
	if (hasattr(driver_part[0]).table, 'tbody')):
		for tr_driver in driver_part[0].table.tbody.children:
			if (tr_driver != '\n'):
				get_driver_info(tr_driver)
				
	for tr_firmware in firmware_part[0].table.tbody.children:
		if (tr_firmware != '\n'):
			get_firmware_info(tr_driver)
		
for key in printers:
	get_driver_or_firmware_info(key, printers[key])

	
log_file.close()