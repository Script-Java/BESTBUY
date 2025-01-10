from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)

class BestBuyScraper:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.48',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
        ]

    def get_bestbuy_search(self, query):
        query_string = query.replace(' ', '+')
        headers = {
            'User-Agent': random.choice(self.user_agents)
        }
        url = f"https://www.bestbuy.com/site/searchpage.jsp?st={query_string}"
        try:
            req = requests.get(url, headers=headers, timeout=10)
            req.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Best Buy: {e}")
            return []

        soup = BeautifulSoup(req.content, 'html.parser')
        search_list = soup.find('ol', {'class': 'sku-item-list'})

        if not search_list:
            print("No search list found.")
            return []

        data_dict_list = []

        items = search_list.find_all('li', {'class': 'sku-item'})
        for item in items:
            try:
                img_tag = item.find('img', {'class': 'product-image'})
                img_src = img_tag['src'] if img_tag else None

                title_container = item.find('h4', {'class': 'sku-title'})
                anchor_tag = title_container.find('a') if title_container else None
                anchor_link = anchor_tag['href'] if anchor_tag else None
                title_text = anchor_tag.text.strip() if anchor_tag else "No Title"

                price_container = item.find('div', {'class': 'priceView-hero-price priceView-customer-price'})
                price = price_container.find('span').text.strip() if price_container else "Price Unavailable"

                data = {
                    "img_src": img_src,
                    "anchor_link": f"https://www.bestbuy.com{anchor_link}" if anchor_link else None,
                    "title": title_text,
                    "price": price,
                }

                data_dict_list.append(data)
            except Exception as e:
                print(f"Error processing an item: {e}")

        return data_dict_list

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    scraper = BestBuyScraper()
    results = scraper.get_bestbuy_search(query)
    return jsonify(results)

if __name__ == "__main__":
    app.run()
