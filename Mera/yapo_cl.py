
# coding: utf-8

# In[18]:

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import re

opts = Options()
opts.set_headless()
assert opts.headless  # operating in headless mode

link="https://www.yapo.cl/biobio/arrendar?ca=9_s&l=0&w=1&cmn=152&cmn=158&cmn=164&cmn=189&cmn=193&ret=2&ps=2&pe=4"

#driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver',options=opts)
driver.set_page_load_timeout(60)
driver.get(link)
driver.maximize_window()
driver.implicitly_wait(20)
#driver.get_screenshot_as_file("Facebook.png")
tabla = driver.find_element_by_id('hl')
tabla = tabla.find_element_by_tag_name('tbody')
items = []
for row in tabla.find_elements_by_xpath(".//tr"):# itera sobre tabla
	
	
	if(len([td.text for td in row.find_elements_by_xpath(".//td[text()]")])>2):
		link = row.find_elements_by_xpath(".//*[@class='redirect-to-url']")[0].get_attribute("href")
		detalle = [td.text for td in row.find_elements_by_xpath(".//td")][2]
		#var = [td.text for td in row.find_elements_by_xpath(".//td[text()]")][2]
		if(len(re.findall('\d+.\d+',detalle))!=0):
			valor = int(re.findall('\d+.\d+',detalle)[0].replace('.',''))
			if( detalle.upper().find("BUSCO") == -1 and detalle.upper().find("PIEZA") == -1 and valor<150000):
				items.append(detalle +" "+str(valor)+" "+link+' \n')	


driver.implicitly_wait(20)

print '\n'.join(items)
#html = tabla.page_source

driver.quit()

#soup = BeautifulSoup(html,'lxml')
#print soup


import smtplib
 
def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
    #print message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()

sendemail(from_addr    = 'mb.us.94@gmail.com', 
    to_addr_list = ['meraulloa@udec.cl'],
    cc_addr_list = [], 
    subject      = 'Arriendos YAPO', 
    message      = ' \n'.join(items).encode('utf-8').strip(), 
    login        = 'mb.us.94@gmail.com', 
    password     = '')


# In[ ]:



