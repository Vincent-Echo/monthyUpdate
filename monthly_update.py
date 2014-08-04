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
