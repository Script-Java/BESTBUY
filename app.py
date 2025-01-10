from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

class BestBuyScraper:
    def get_bestbuy_search(self, query):
        query_string = query.replace(' ', '+')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        url = f"https://www.bestbuy.com/site/searchpage.jsp?st={query_string}"
        req = requests.get(url, headers=headers)

        if req.status_code != 200:
            return []

        soup = BeautifulSoup(req.content, 'html.parser')
        search_list = soup.find('ol', {'class': 'sku-item-list'})

        if not search_list:
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
    app.run(debug=True)
