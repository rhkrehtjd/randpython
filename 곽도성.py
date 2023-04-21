from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

store_name = []
si_do = []
gun_gu = []
address = []

webdriver_path = '/Users/gwagdoseong/Documents/Rprogramming/chromedriver.exe'

base_url = 'https://www.kyochon.com/shop/domestic.asp?sido1=1&sido2=1'
browser = webdriver.Chrome(executable_path=webdriver_path)
browser.get(base_url)
html = browser.page_source
soupKyochon = BeautifulSoup(html, 'html.parser')

select_sido1 = soupKyochon.find('select', {'id': 'sido1'})
options_sido1 = select_sido1.find_all('option')

sido_dict = {}
gungu_dict = {}

for option in options_sido1:
    key = int(option['value'])
    value = option.text
    sido_dict[key] = value

for selected_sido1 in range(1, 18):
    sido1_dropdown = Select(browser.find_element('id', 'sido1'))
    sido1_dropdown.select_by_value(str(selected_sido1))

    time.sleep(1)

    html = browser.page_source
    soupKyochon = BeautifulSoup(html, 'html.parser')

    select_sido2 = soupKyochon.find('select', {'id': 'sido2'})
    options_sido2 = select_sido2.find_all('option')

    for option in options_sido2:
        key = (selected_sido1, int(option['value']))
        value = option.text
        gungu_dict[key] = value

browser.quit()

def get_store_info(url, sido, gungu):
    html = urllib.request.urlopen(url)
    soupKyochon = BeautifulSoup(html, 'html.parser')
    tag_ul = soupKyochon.find('ul', attrs={'class':'list'})
    tag_strong = tag_ul.find_all('strong') # store name
    tag_em = tag_ul.find_all('em') # store address
    
    for i in range(len(tag_strong)):
        # store name
        store_name_text = tag_strong[i].text
        store_name.append(store_name_text)

        # si_do
        sido_value = sido_dict[sido]
        si_do.append(sido_value)
        
        # gun_gu
        gungu_value = gungu_dict[(sido, gungu)]
        gun_gu.append(gungu_value)
        
        # address
        address_text = tag_em[i].text

        p_space = re.compile(r'[\s\t]+')
        address_text = re.sub(p_space, ' ', address_text)
        address_text = address_text.strip()

        p_tp = re.compile(r'\s\d{2,3}-\d{3,4}-\d{4}')
        address_text = re.sub(p_tp, '', address_text)

        address.append(address_text)

for sido1 in range(1, 4):
    for sido2 in range(1, 4):
        try:
            Kyochon_url = f'https://www.kyochon.com/shop/domestic.asp?sido1={sido1}&sido2={sido2}'
            get_store_info(Kyochon_url, sido1, sido2)
        except:
            break

data = {'store': store_name, 'sido': si_do, 'gungu': gun_gu, 'store_address': address}
kyochon_df = pd.DataFrame(data)
kyochon_df.to_csv("/Users/gwagdoseong/Documents/Rprogramming/kyochon.csv", encoding = "cp949", mode = "w", index = True)