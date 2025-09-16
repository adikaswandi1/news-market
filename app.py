from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

headers = {
    'User -Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/114.0.0.0 Safari/537.36'
}

urls = [
    'https://market.bisnis.com/',
    'https://www.idxchannel.com/market-news/',
    'https://www.cnbcindonesia.com/research'
]

def scrape_headlines(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, 'html.parser')

            if 'market.bisnis.com' in url:
                headlines = soup.find_all('a', class_='flashnewsLink')
            elif 'idxchannel.com' in url:
                headlines = soup.find_all(['a', 'h2'], class_=['headline-kanal', 'list-berita-baru'])
            elif 'cnbcindonesia.com' in url:
                headlines = soup.find_all('h2', class_='line-clamp-3')
            else:
                headlines = []

            return [headline.get_text(strip=True) for headline in headlines]
        else:
            return []
    except requests.exceptions.RequestException:
        return []

@app.route('/')
def home():
    all_headlines = {}
    for url in urls:
        all_headlines[url] = scrape_headlines(url)
    return render_template('index.html', all_headlines=all_headlines)

if __name__ == '__main__':
    app.run(debug=True)