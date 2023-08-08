from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup


def scr_last_page(x): #Find last page number on a website page, x = url
    chrome_options = Options()
    chrome_options.add_argument('disable-notifications')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('start-minimized')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--silent')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)
    # driver.minimize_window()

    driver.get(x)
    driver.implicitly_wait(60)
    # print('Page Loaded_______')

    action = ActionChains(driver)
    action.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
    time.sleep(1)
    # print("STARTING PANGING DOWN =============") #just to monitor terminal
    con = 0
    while con < 12:
        action.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
        time.sleep(0.5)
        con += 1
        # print(con)
    # print("DONE PANGING DOWN =============")

    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html, "html.parser")

    #Find last page
    paging = soup.find_all('button', class_='css-bugrro-unf-pagination-item')
    pag = [i.text for i in paging]
    try:
        last_page = int(pag[-1].replace('.',''))
    except:
        last_page = pag
    driver.close()

    return last_page

def scr_list_page(x,y): #get list of all pages from 1, x = last page (int), y = page url
    li = []
    reng = list(range(1,x))
    for i in reng:

        url = y.replace('page=2',f'page={i}')
        # url = f'https://www.tokopedia.com/search?page={i}&q=kaos%20polos&st=product'
        li.append(url)
    return li

def scr_prod(x): #Get all product link inside grid, x = url page from scr_list_page
    chrome_options = Options()
    chrome_options.add_argument('disable-notifications')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('start-minimized')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--silent')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)
    # driver.minimize_window()
    # TOKPED
    driver.get(x)
    driver.implicitly_wait(60)
    # print('Page Loaded_______')

    action = ActionChains(driver)
    action.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
    time.sleep(1)
    # print("STARTING PANGING DOWN =============") #just to monitor terminal
    con = 0
    while con < 12:
        action.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
        time.sleep(0.5)
        con += 1
        # print(con)
    # print("DONE PANGING DOWN =============")

    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html, "html.parser")

    #Get each product link
    prod_grid = soup.find_all('div', class_='css-12sieg3')
    link_prod = []
    for i in prod_grid:
        link = i.find('a').get('href')
        link_prod.append(link)
        # print(link)
    # print(len(link_prod))
    driver.close()
    return link_prod #output are list with specific product page

def scr_sub(x,y): #Get all data variable each product, x = url specific product, y = time sleep (int)
    
    chrome_options = Options()
    chrome_options.add_argument('disable-notifications')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('start-minimized')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--silent')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)
    driver.minimize_window()
    driver.get(x)
    driver.implicitly_wait(60)
    # print(f'Page Loaded_______')

    #This line are paging down process to load all pages
    action = ActionChains(driver)
    action.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
    time.sleep(y)
    # print("STARTING PANGING DOWN =============") #just to monitor terminal
    con = 0
    while con < 2:
        action.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
        time.sleep(y)
        con += 1
        # print(con)
    # print("DONE PANGING DOWN =============")

    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find('h1', class_='css-1os9jjn').text
    price = soup.find('div',class_='price').text
    spa = soup.find('div',class_='items').text
    spa = spa.split()
    sold = (spa[1]+spa[2]).split('+')[0]
    rate = spa[3]
    rate_count = spa[4]
    discuss = spa[-1]
    description = soup.find('div',class_='css-16inwn4').text
    toko = soup.find('div', class_='css-k008qs').text
    lokasi = soup.find('div', class_='css-1yuhvjn').text
    lokasi = lokasi.split()[2:4]
    # print('VARIABLE GET ========')
    data = {'nama': [title],
            'harga':[price],
            'span':[spa],
            'Deskripsi':[description],
            'Nama Toko':[toko],
            'Lokasi Toko':[lokasi],
            'link':[x]}
            
    driver.close()

    return data #output are dict ready to make DataFrame

