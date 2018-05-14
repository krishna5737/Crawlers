#Import required libraries
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time

#start firefox browser drvier
driver = webdriver.Firefox()
City = input('Please enter city you want to crawl: ').title()
keyword = input('Please enter the keword you want to crawl: ').title()
pages_to_crawl = int(input('Please enter maximum number of pages you want to crawl: '))


#function to convert div to number because in JD they have encrypted the contact details of client
def extract_contact_number(contact_info):
	r = []
	contact_info = list(str(contact_info).split("icon-"))
	for i in contact_info[1:]:
		r.append(i[:2])
	r = [a.replace('dc', '+').replace('ba', '-').replace('ji', '9').\
		replace('lk', '8').replace('nm','7').replace('po','6').replace('rq','5').\
		replace('ts', '4').replace('vu', '3').replace('wx', '2').replace('yz', '1').\
		replace('ac','0').replace('fe','(').replace('hg',')') for a in r]
	return(''.join(r))

# Ad headers to csv file
fields = ['Page', 'City','Name', 'Phone']
output_file_name = 'result_'+ City +'_'+keyword+'.csv' 
out_file = open(output_file_name,'w')
csvwriter = csv.writer(out_file)
header = 'Page','City','Dealer Name','Contact Number'
csvwriter.writerow(header)
#####headers added

page_number = 1 # crawling to starts from
flag = True # flag to check weather maximum results are reached or not


while(flag == True and page_number < pages_to_crawl):
	url = 'https://www.justdial.com/'+City+'/'+ keyword +'/page' + '-' + str(page_number)
	print("Crawling Page -", page_number)
	driver.get(url)
	scrolls = 3

	#scroll the page and load the data in soup variable
	for i in range(1,scrolls):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(2)
		html = driver.page_source
		soup = BeautifulSoup(html,"lxml")
	

	if(not (soup.select('.cntanr'))):
		flag = False
	
	
	City = str(driver.current_url).split('/')[3]
	for containers in soup.select('.cntanr'):
		if(containers):
			contact_infos = 'Contact Number not available'
			names = str(containers.select('.lng_cont_name'))[29:-8]
			for contact_info in containers.find_all('p',class_="contact-info"):
				contact_infos = extract_contact_number(contact_info)
			dict_service = [page_number,City,str(names),contact_infos]
			csvwriter.writerow(dict_service)

	page_number+=1			


driver.quit()
