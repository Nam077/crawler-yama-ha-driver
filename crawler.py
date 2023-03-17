import json
import re
import time
from datetime import datetime

import pyautogui
import requests as req
from bs4 import BeautifulSoup as bs
import os

proxies = ['200.54.194.13:53281', '45.42.177.58:3128', '200.105.215.22:33630', '86.120.122.3:3128',
           '190.61.88.147:8080']
proxies_list = []
for proxy in proxies:
    proxies_list.append({'http': 'http://' + proxy, 'https': 'https://' + proxy})

open_status = 'open'


class Crawler:
    def __init__(self, url, name=None, save_file=False, open_status=False):
        self.headers = None
        self.url = url
        self.path = None
        self.open_status = open_status
        self.name = name
        self.save_file = save_file
        self.open_vpn = 'open'
        self.soup = None

    def open_windscribe(self):
        os.startfile('C:\\Program Files\\Windscribe\\Windscribe.exe')
        time.sleep(3)
        x = 1154
        y = 455
        if not self.open_status:
            pyautogui.click(x=x, y=y)
        if self.open_status:
            time.sleep(3)
            pyautogui.click(x=x, y=y)
        self.open_status = True

    def get_soup(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }
        if self.name is None:
            self.name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        try:
            response = req.get(self.url, headers=self.headers)
            response.raise_for_status()  # raise an exception if status code is not 200
        except req.exceptions.RequestException as e:
            print(e)
            self.soup = None
            return

        self.soup = bs(response.text, 'html.parser')
        # save response to html file
        if not os.path.exists('data/'):
            os.makedirs('data/')
        self.path = 'data/'
        if self.save_file:
            if not os.path.exists('data/html'):
                os.makedirs('data/html')
            if not os.path.exists('data/html/' + self.name):
                os.makedirs('data/html/' + self.name)

            with open(self.path + '/html/' + self.ame + '.html', 'w', encoding='utf-8') as f:
                f.write(response.text)

    def get_title(self):
        if not self.soup:
            return None
        title = self.soup.find('title')

    # Tìm tất cả các thẻ div có class là SecOneSubSectionContainer
    # những thẻ này chứa tên của các element
    def get_children_s(self):
        self.get_soup()
        if not self.soup:
            return None
        children_s = self.soup.find_all('div', {'class': 'SecOneSubSectionContainer'})
        result = []
        for children in children_s:
            name = children.text.strip()
            link = children.find('a', target='_top').get('href')
            image_element = children.find('img',
                                          id=lambda value: value and value.startswith('SecOneSubActSecImage_Small'))
            image_src = children.find('img', 'SecOneSubActSecImage').get('src') if image_element else None
            full_name = image_element.get('alt') if image_element else None
            result.append({'name': name, 'link': link, 'full_name': full_name, 'image_src': image_src})
            # save json file
        return result

    # Lấy thông tin của các element con
    def get_infor_children(self):
        children_s = self.get_children_s()
        if not children_s:
            return []
        i = 0

        for children in children_s:
            i += 1
            print(i)
            link = children['link']
            response = req.get(link, headers=self.headers)
            response.raise_for_status()
            soup = bs(response.text, 'html.parser')
            image_main = soup.find('image', id='svg_gg')
            image_main = image_main.get('xlink:href') if image_main else None

            if not os.path.exists(self.path + '/json'):
                os.makedirs(self.path + '/json')
            if self.save_file:
                if not os.path.exists(self.path + 'html/' + self.name + '/children'):
                    os.makedirs(self.path + 'html/' + self.name + '/children')
                children_name_file = re.sub(r'[^\w\s]', '', children['name'])
                with open(self.path + 'html/' + self.name + '/children/' + children_name_file + '.html', 'w',
                          encoding='utf-8') as f:
                    f.write(response.text)
            rows = soup.find_all('tr', class_='parts_list_row')
            nameChildren = soup.find('div', class_='parts_list_Section_Name')
            nameChildren = nameChildren.text if nameChildren else None
            children.update({'nameChildren': nameChildren})
            result = []
            print(children['name'])
            print(children['link'])
            for row in rows:

                try:
                    # parts_list_HLSM_PartNo
                    parts_list_HLSM_PartNo = row.find('input', class_='parts_list_HLSM_PartNo')
                    parts_list_HLSM_PartNo = parts_list_HLSM_PartNo.get('value') if parts_list_HLSM_PartNo else None
                    # parts_list_PartNo
                    parts_list_PartNo = row.find('input', class_='parts_list_PartNo')
                    parts_list_PartNo = parts_list_PartNo.get('value') if parts_list_PartNo else None
                    # parts_list_PartNo_RefNo
                    parts_list_PartNo_RefNo = row.find('input', class_=lambda value: value and value.startswith(
                        'parts_list_PartNo_RefNo'))
                    parts_list_PartNo_RefNo = parts_list_PartNo_RefNo.get('value') if parts_list_PartNo_RefNo else None
                    # parts_list_RefNo
                    parts_list_RefNo = row.find('td', id=lambda value: value and value.startswith('parts_list_RefNo'))
                    parts_list_RefNo = parts_list_RefNo.text if parts_list_RefNo else None
                    # parts_list_descrip
                    parts_list_descrip = row.find('td', class_='parts_list_descrip')
                    parts_list_descrip = parts_list_descrip.text if parts_list_descrip else None
                    # parts_list_SalePrice
                    parts_list_SalePrice = row.find('td', id := lambda value: value and value.startswith(
                        'parts_list_SalePrice'))
                    parts_list_SalePrice = parts_list_SalePrice.text if parts_list_SalePrice else None
                    # parts_list_QtyReq
                    parts_list_QtyReq = row.find('td', class_='parts_list_QtyReq')
                    parts_list_QtyReq = parts_list_QtyReq.text if parts_list_QtyReq else None
                    result.append({
                        'parts_list_HLSM_PartNo': parts_list_HLSM_PartNo,
                        'parts_list_PartNo': parts_list_PartNo,
                        'parts_list_PartNo_RefNo': parts_list_PartNo_RefNo,
                        'parts_list_RefNo': parts_list_RefNo,
                        'parts_list_descrip': parts_list_descrip,
                        'parts_list_SalePrice': parts_list_SalePrice,
                        'parts_list_QtyReq': parts_list_QtyReq,
                        'image_main': image_main,
                    })
                except Exception as e:
                    print(e)
                    continue
            children.update({'infor': result})
            # print(children)

            with open(self.path + '/json/' + self.name + '.json', 'w', encoding='utf-8') as f:
                json.dump(children_s, f, indent=4, ensure_ascii=False)
        return children_s


# muốn lưu file html thì truyền thêm save_file=True (mặc định là False)
# muốn lưu file theo tên thì truyền thêm name (mặc định là None)
# crawler = Crawler(url_,name='suzuki')
# truyền thêm tên file json
datas = [
    {'url': 'https://onlinemicrofiche.com/riva_normal/showmodel/13/yamahaatv/788', 'name': None},
    {'url': 'https://onlinemicrofiche.com/riva_normal/showmodel/13/yamahaatv/785', 'name': 'yanaha'},

]

for data in datas:
    check = True
    while check:
        if data['name'] and data['name'] != '' and data['name'] is not None:
            crawler = Crawler(data['url'], name=data['name'])
        else:
            crawler = Crawler(data['url'])
        result = crawler.get_infor_children()
        if not result:
            crawler.open_windscribe()
            time.sleep(5)
        else:
            check = False
