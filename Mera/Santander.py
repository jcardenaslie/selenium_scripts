

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
import re
path = "/Users/meraioth/selenium_test/"

opts = Options()
opts.set_headless()
assert opts.headless  # operating in headless mode

random.seed(datetime.now())

link="https://www.santander.cl"

driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver',options=opts)
#driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
driver.set_page_load_timeout(50)
time.sleep(random.randint(180,1600))
driver.get(link)
driver.maximize_window()
driver.implicitly_wait(20)
#driver.get_screenshot_as_file("Facebook.png")
driver.find_element_by_id('d_rut').send_keys('18.685.628-7')
driver.find_element_by_id('d_pin').send_keys('')
driver.find_element_by_id('botonenvio').click()
#driver.get_screenshot_as_file("Fabook_login.png")
#driver.implicitly_wait(20)
time.sleep(random.randint(5,60)) 
driver.get('https://www.santander.cl/transa/productos/divisa/dolar.asp?tipo_tx=0')
# driver.switch_to_frame("frame2")
# driver.find_element_by_id("IN1").click()
# time.sleep(random.randint(5,60)) 
# driver.find_element_by_id("DO2").click()
# driver.switch_to_frame("p4")
# driver.implicitly_wait(10)
# time.sleep(random.randint(5,60)) 
# driver.find_element_by_name("comprar").click()
# driver.implicitly_wait(20)
#driver.find_element_by_xpath('/html/body/center/table/tbody/tr/td/form/table/tbody/tr/td/table/tbody/tr/td[1]/a/img')
# dolar= driver.find_element_by_id("oDolar").text
#print dolar
html = driver.page_source
time.sleep(random.randint(5,60)) 
driver.quit()

#soup = BeautifulSoup(html,'lxml')
dolar = float(re.search(r'\bValorDolar: \b(\d+.\d)', html).group(1).replace(',','.'))
print dolar
# data = driver.find_elements_by_tag_name('span')
# print(data)


# In[21]:

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
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()


# import re

# dolar =  int(re.search(r'\d+', dolar).group())

if dolar < 605 :
    sendemail(from_addr    = 'mb.us.94@gmail.com', 
          to_addr_list = ['meraulloa@udec.cl'],
          cc_addr_list = [], 
          subject      = 'Valor Dolar ', 
          message      = str(dolar), 
          login        = 'mb.us.94@gmail.com', 
          password     = '')




# In[ ]:



