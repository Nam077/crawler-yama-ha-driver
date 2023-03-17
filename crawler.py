import json
from datetime import datetime

import requests as req
from bs4 import BeautifulSoup as bs

proxies = ['200.54.194.13:53281', '45.42.177.58:3128', '200.105.215.22:33630', '86.120.122.3:3128',
           '190.61.88.147:8080']
proxies_list = []
for proxy in proxies:
    proxies_list.append({'http': 'http://' + proxy, 'https': 'https://' + proxy})


class Crawler:
    def __init__(self, url, name=None):
        self.url = url
        self.name = name
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }
        try:

            response = req.get(url, headers=self.headers)

            response.raise_for_status()  # raise an exception if status code is not 200
        except req.exceptions.RequestException as e:
            print(e)
            self.soup = None

            return

        self.soup = bs(response.text, 'html.parser')
        # save response to html file
        with open('response.html', 'w', encoding='utf-8') as f:
            f.write(self.soup.prettify())

    def get_title(self):
        if not self.soup:
            return None
        title = self.soup.find('title')

    # Tìm tất cả các thẻ div có class là SecOneSubSectionContainer
    # những thẻ này chứa tên của các element
    def get_children_s(self):
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
        if not self.soup:
            return None
        children_s = self.get_children_s()
        i = 0
        name_file = ''
        if self.name is not None:
            name_file = self.name
        else:
            name_file = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        for children in children_s:
            i += 1
            print(i)
            link = children['link']
            response = req.get(link, headers=self.headers)
            response.raise_for_status()  # raise an exception if status code is not 200
            soup = bs(response.text, 'html.parser')
            image_src = soup.find('image', id='svg_gg').get('xlink:href')
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
                    # image_src
                    # end
                    result.append({
                        'parts_list_HLSM_PartNo': parts_list_HLSM_PartNo,
                        'parts_list_PartNo': parts_list_PartNo,
                        'parts_list_PartNo_RefNo': parts_list_PartNo_RefNo,
                        'parts_list_RefNo': parts_list_RefNo,
                        'parts_list_descrip': parts_list_descrip,
                        'parts_list_SalePrice': parts_list_SalePrice,
                        'parts_list_QtyReq': parts_list_QtyReq,
                        'image_src': image_src
                    })
                except Exception as e:
                    print(e)
                    continue
            children.update({'infor': result})
            print(children)

            with open('data/' + name_file + '.json', 'w', encoding='utf-8') as f:
                json.dump(children_s, f, indent=4, ensure_ascii=False)
        return children_s


url_ = 'https://onlinemicrofiche.com/riva_normal/showmodel/13/suzukiatv/406'

crawler = Crawler(url_)
# crawler = Crawler(url_,name='suzuki')
# truyền thêm tên file json
print(crawler.get_infor_children())
