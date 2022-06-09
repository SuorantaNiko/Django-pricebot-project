from bs4 import BeautifulSoup
import requests, re
from datetime import datetime

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

def search_product_list(url):

    
    now = datetime.now().strftime('%Y-%m-%d %Hh%Mm')

    page = requests.get(url, headers=HEADERS)

    Soup = BeautifulSoup(page.content, features="lxml")
    soup = BeautifulSoup(page.content, 'html.parser')
        
    title = soup.find(id='productTitle').get_text().strip()
    Img = Soup.find(id='imgTagWrapperId').get_text().strip()
    Price = soup.find(id='corePrice_desktop').text
    Price = re.sub('\n', '', Price).strip()
    prices =    {'default' : 0,
                    'discount' : 0,
                    'save' : 0}
    prices['default'] = float(Price[Price.index('$')+1:Price.find('$', Price.find('$')+1)])
        
        
    try:
        Price = Price[Price.find('$', Price.find('$')+1)+1:]
        print(Price)
        prices['discount'] = float(Price[Price.index('$')+1:Price.find('$', Price.find('$')+1)])
        Price = Price[Price.find('$', Price.find('$')+1)+1:]
        print(Price)
        prices['save'] = float(Price[Price.index('$')+1:Price.find('$', Price.find('$')+1)])
    except:
        prices['discount'] = 0
        prices['save'] = 0

        
    try: 
        all_imgs = soup.find_all('img')
            
        for i in all_imgs:
            if i['alt'] == title:
                print('FOUND!')
                Img = i
                break

        Img = str(Img)
        Img = Img[Img.index('{')+2:Img.index('"')]
    except:
        Img = ''

    try:
        soup.select('#availability .a-color-state')[0].get_text().strip()
        stock = 'Out of Stock'
    except:
        try:
            soup.select('#availability .a-color-price')[0].get_text().strip()
            stock = 'Out of Stock'
        except:
            stock = 'Available'


    product =   {'date': now.replace('h',':').replace('m',''),
                'jpg' : Img,
                'url': url,
                'title': title,
                    
                'price': prices,
                'stock': stock}

        
    return product

def main():
    url = "https://www.amazon.com/Fiodio-Wireless-Mechanical-Keyboard-F-SG61/dp/B09KHK3TB6/ref=sr_1_1_sspa?keywords=gaming+keyboard&pd_rd_r=fc5eb77e-9f69-4f9b-8ecc-862bdf7c9f21&pd_rd_w=OwyiY&pd_rd_wg=pTCOt&pf_rd_p=12129333-2117-4490-9c17-6d31baf0582a&pf_rd_r=3CX2A2GYRQNYDAT9T1Q2&qid=1648124262&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFHSzUxSzkwUUNHT0smZW5jcnlwdGVkSWQ9QTA4OTcyMTgyTEs0UFVCM0Q3SlVJJmVuY3J5cHRlZEFkSWQ9QTA5NjI3MDQyODM4VTY3Q04yR05PJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=="
    search_product_list(url)
if __name__ == "__main__":
    main()