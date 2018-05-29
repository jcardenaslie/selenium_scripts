from urllib.request import Request, urlopen
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
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

regions= {'15':'https://www.yapo.cl/region_metropolitana',
         '1':'https://www.yapo.cl/arica_parinacota',
         '2':'https://www.yapo.cl/tarapaca',
         '3':'https://www.yapo.cl/antofagasta',
         '4':'https://www.yapo.cl/atacama',
         '5':'https://www.yapo.cl/coquimbo',
         '6':'https://www.yapo.cl/valparaiso',
         '7':'https://www.yapo.cl/ohiggins',
         '8':'https://www.yapo.cl/maule',
         '9':'https://www.yapo.cl/biobio',
         '10':'https://www.yapo.cl/araucania',
         '11':'https://www.yapo.cl/los_rios',
         '12':'https://www.yapo.cl/los_lagos',
         '13':'https://www.yapo.cl/aisen',
         '14':'https://www.yapo.cl/magallanes_antartica'}
search_parameters ={'product':'notebook','region':9}
path="C:/Users/jquin/Desktop/ScrapBanco/Utilities"
search_item= 'ps4'


#selenium+ input de producto
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

opts = Options()
opts.set_headless()
assert opts.headless  # operating in headless mode

region_index=9
link=regions[str(region_index)]

driver = webdriver.Firefox(executable_path=r'C:/Users/jquin/Desktop/gecko_driver/geckodriver.exe',options=opts)
driver.get(link)
driver.maximize_window()
driver.implicitly_wait(10)
driver.find_element_by_id('searchtext').send_keys(search_item)
# b.find_element_by_xpath("//select[@name='w']/option[value()="+ link=regions[str(region_index)][0]+"]").click()
driver.find_element_by_xpath("//select[@name='cg']/option[@value='3020']").click()

# driver.find_element_by_xpath("//select[@name='ps']/option[@value='5']").click()

# if min_price != None:
#     driver.find_element_by_xpath("//select[@name='ps']/option[@value='5']").click()
# if max_price != None:
#     pass
#     driver.find_element_by_xpath("//select[@name='pe']/option[text()='$ 100.000']").click()

driver.find_element_by_id('searchbutton').click()

html = driver.page_source

driver.implicitly_wait(10)
driver.quit()

soup = BeautifulSoup(html, 'lxml')

import yapo_scrap_lib as yaplib

products_links, products_new = yaplib.get_products_links(soup)

email_string = ""
for product in products_new:
    email_string+=" ".join(product[1:]) + "\n"


if len(products_new) > 0:
   sendemail(from_addr    = 'jcardenas.lie@gmail.com', 
       to_addr_list = ['jcardenas.lie@gmail.com'],
       cc_addr_list = [], 
       subject      = 'Ultimos '+ search_item+ ' YAPO', 
   #     message      = ' \n'.join(products_new).encode('utf-8').strip(), 
       message      = email_string, 
       login        = 'jcardenas.lie@gmail.com', 
       password     = 'Scott9876..')

print('finish without errors')