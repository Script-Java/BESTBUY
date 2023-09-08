from bs4 import BeautifulSoup
import requests

class BestBuy_scraper:
    def __init__(self):
        pass
        
    def get_bestbuy_search(query):
        query_string = query.replace(' ', '+')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        url = f"https://www.bestbuy.com/site/searchpage.jsp?st={query_string}"
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.content,'html.parser')
        search_list = soup.find('ol', {'class':'sku-item-list'})
        col_left = soup.find_all('div', {'class':'column-left'})
        col_middle = soup.find_all('div', {'class':'column-middle'})
        col_right = soup.find_all('div', {'class':'column-right'})


        data_dict_list = []
        anchor_links = []
        img_links = []
        title_name_list = []
        price_lists = []

        for i in search_list:
            for x in col_left:
                a_link = x.find('a',{'class':'image-link'})
                anchor_links.append(a_link)
                img_link = x.find('img', {'class':'product-image'})
                img_links.append(img_link)
            for d in col_middle:
                b_title_container = d.find('h4', {'class':'sku-title'})
                b_title = b_title_container.find('a')
                title_name_list.append(b_title)
            for j in col_right:
                price_container = j.find('div', {'class':'priceView-hero-price priceView-customer-price'})
                price = price_container.find('span')
                price_lists.append(price)

        for link, img, name, price in zip(anchor_links, img_links, title_name_list, price_lists):
            data = {
                "img_src": img['src'],
                "anchor_link": link['href'],
                "title": name.text,
                "price": price.text,
            }

            data_dict_list.append(data)



        return data_dict_list

print(get_bestbuy_search('3070 ti'))




