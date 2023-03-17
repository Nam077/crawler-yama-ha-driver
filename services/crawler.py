import requests as req
from bs4 import BeautifulSoup as bs
import requests.exceptions


class Crawler:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }
        try:
            response = req.get(url, headers=self.headers)
            response.raise_for_status()  # raise an exception if status code is not 200
        except requests.exceptions.RequestException as e:
            print(e)
            self.soup = None
            return
        self.soup = bs(response.text, 'html.parser')
        # save response to html file

    def get_title(self):
        if not self.soup:
            return None
        title = self.soup.find('title')
        return title.text if title else None

    def get_description(self):
        if not self.soup:
            return None
        description = self.soup.find('meta', attrs={'name': 'description'})
        return description['content'] if description else None

    def get_keywords(self):
        if not self.soup:
            return None
        keywords = self.soup.find('meta', attrs={'name': 'keywords'})
        return keywords['content'] if keywords else None

    def get_image(self):
        if not self.soup:
            return None
        image = self.soup.find('meta', attrs={'property': 'og:image'})
        return image['content'] if image else None

    def get_links(self):
        if not self.soup:
            return None
        links = self.soup.find_all('a')
        return [link.get('href') for link in links]

    def get_divs_by_class(self, class_name):
        if not self.soup:
            return None
        divs = self.soup.find_all('div', {'class': class_name})
        return [div.text.strip() for div in divs if div.text.strip()]

    def get_yt_formatted_string(self):
        if not self.soup:
            return None
        yt_formatted_string = self.soup.find_all('a',
                                                 attrs={'class': 'yt-simple-endpoint style-scope ytd-video-renderer'})
        return yt_formatted_string[0].text.strip() if yt_formatted_string else None


crawler = Crawler(url='https://www.youtube.com/results?search_query=t%C6%B0%C6%A1ng+t%C6%B0+th%C3%A0nh+h%E1%BB%8Da')
print(crawler.get_image())
