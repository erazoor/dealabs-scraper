from bs4 import BeautifulSoup
import requests


class DealScraper:
    def __init__(self, start_page=1, end_page=50, targeted_temperature=1000):
        self.start_page = start_page
        self.end_page = end_page
        self.targeted_temperature = targeted_temperature
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) ' +
                          'Chrome/89.0.4389.82 Safari/537.36'}

    def scrap(self):
        for i in range(self.start_page, self.end_page + 1):
            url = f'https://www.dealabs.com/groupe/high-tech?page={i}'
            response = requests.get(url, headers=self.headers)
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')
            self.parse_page(soup, i)

    def parse_page(self, soup, page_number):
        for deal in soup.find_all('article', class_='thread--deal'):
            try:
                title = deal.find('a', class_='thread-title--list')['title']
                price = deal.find('span', class_='thread-price')
                link = deal.find('a', class_='thread-title--list')['href']
                temperature = deal.find('span', class_='vote-temp--hot')
                expired = deal.find('span', class_='cept-show-expired-threads')

                if expired or not temperature or not price:
                    continue

                price = [p for p in price][0]
                temperature = int(''.join(char for chars in temperature for char in chars if char.isdigit()))

                if temperature >= self.targeted_temperature:
                    print(f'{temperature} \n{title} \n{price} \npage : {page_number} \n{link} \n')

            except Exception as e:
                print(e)
                continue


if __name__ == '__main__':
    scraper = DealScraper()
    scraper.scrap()
