from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def url_to_selenium(url):
    opts = Options()
    opts.set_headless()
    assert opts.headless  # operating in headless mode

    region_index=9

    driver = webdriver.Firefox(executable_path=r'C:/Users/jquin/Desktop/gecko_driver/geckodriver.exe',options=opts)
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(10)

    html2 = driver.page_source
    driver.quit()
    
    return  BeautifulSoup(html,'lxml')

def url_to_soup(url):
    proxies_req = Request(url)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')
    soup = BeautifulSoup(proxies_doc, 'html.parser')
    return soup

#get paginations
def get_pagination_links(soup):
    paginations = soup.find('div',class_='resultcontainer').find_all('span')
    if len(paginations) == 0:
        return list()
    else:
        pages_links = []
        for anchor in paginations[1:]:
            pages_links.append(anchor.a.get('href'))
        return pages_links

#la carga de request es solo la cantidad de paginas

def get_all_products_links(initial_soup):
    #arreglo que almacenara todos los productos
    all_products_links= []
    #recupero los links de las paginas que contienen los productos
    product_pages = get_page_links(initial_soup)
    # el primer soup tiene informacion de la primera pagina, la reutilizamos
    all_products_links.append(get_page_products_links(initial_soup))
    
    #trasnformarmos todas las urls de las paginas a soups, menos la primera pagina que ya la extragimos
    if len(product_pages) == 0:
        return all_products_links
    
    soups = []
    for page_link in product_pages[1:]:
        soups.append(url_to_selenium(page_link))
    
    #ahora para cada soup extraemos sus productos
    for soup in soups:
        all_products_links.append(get_page_products_links(soup))
        
    return all_products_links

def get_products_links(soup):
    products_items = soup.find('table',class_='listing_thumbs').tbody.find_all('tr')
    products_links = []
    products_new = []
    for item in products_items:

        if item.find_all('td', class_='listing_thumbs_date') == []:
            continue
            
        item_date= item.find_all('td', class_='listing_thumbs_date')[0].find_all('span',class_='date')[0].text
        info = item.find_all('td', class_='thumbs_subject')[0]
        item_name= info.a.text
        
        if info.span != None:
            item_price= info.span.text
        item_url = item.find_all('a', class_='redirect-to-url')
        
        if len(item_url) > 0:
            products_links.append(item_url[0].get('href'))
        if item_date == 'Hoy':
            products_new.append([item_date, item_name, item_price, item_url[0].get('href')])
        
    
    return products_links, products_new

def get_product_content(url):
    soup = url_to_selenium(url)
    
    nombre = soup.find('div', class_='title-main').h1.text
    publish_date = soup.find('div', class_='title-main').small.time.text
    price = soup.find('div', class_='price text-right')
    location = soup.find('p', class_='map-region').span.text.split(',')
    description= soup.find('div', class_='description').p.text
    details_name = soup.find('div', class_='details').table.find_all('th')
    details_value = soup.find('div', class_='details').table.find_all('td')