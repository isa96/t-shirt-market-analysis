
from tqdm import tqdm
import pickle
import scrape_main as sm

#Pickle function to save and load
def picle_save(x,y):
    with open(x, 'wb') as file:
        pickle.dump(y, file)
def pickle_load(x):
    with open(x, 'rb') as file:
        myvar = pickle.load(file)
    return myvar

#URL
main_url = 'https://www.tokopedia.com/search?st=product&q=kaos%20polos&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource='
page_url = 'https://www.tokopedia.com/search?navsource=&page=2&q=kaos%20polos&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=product'

#Last page
last_page = sm.scr_last_page(main_url)

#Page link
page_link = sm.scr_list_page(last_page,page_url)

#Product link
prod_link = []
for i in page_link:
    prod_link += sm.scr_prod(i)

#Blank dict to gather all dict from scraping
data_dict= {'nama': [],
            'harga':[],
            'span':[],
            'Deskripsi':[],
            'Nama Toko':[],
            'Lokasi Toko':[],
            'link':[]}


#load dict in case continuing the process
data_dict = pickle_load('data_dict.pkl')
done_link = pickle_load('done_link.pkl')
fail_link = pickle_load('fail_link.pkl')
prod_link = pickle_load('prod_link.pkl')


count = 0
for i in tqdm(prod_link):
    count += 1
    if i not in done_link: #skip scrapped link
        try:
            dif = sm.scr_sub(i,1)

            for key in data_dict:
                data_dict[key].append(dif[key][0])
            done_link.append(i)

        except:
            pass
            fail_link.append(i) #pass the fail link
    else:
        pass
    #save all data
    picle_save('data_dict.pkl',data_dict)
    picle_save('done_link.pkl',done_link)
    picle_save('fail_link.pkl',fail_link)

