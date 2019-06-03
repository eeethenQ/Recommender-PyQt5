import requests
import csv
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup

from skimage import io, transform
import numpy as np
from tqdm import tqdm

def get_html_content(url , data = None):
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }
    timeout = random.choice(range(8, 18))
    while True:
        try:
            rep = requests.get(url,headers = header,timeout = timeout)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print( '3:', e)
            time.sleep(random.choice(range(8,15)))

        except socket.error as e:
            print( '4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print( '5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print( '6:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text

def save_img(path, id_list):
    img_list = []
    for i in tqdm(id_list):
        # print(i)
        movie_url = "https://www.imdb.com/title/tt00{}/".format(i)
        html_content = get_html_content(movie_url)
        bs = BeautifulSoup(html_content, "html.parser")
        body = bs.body
        img_src = body.find('div', {'class' : 'poster'}).find('img').get('src')
        if img_src == "":
            print("Wrong poster url")
        
        image = io.imread(img_src)
        img_list.append(image)

    img_output = np.concatenate(img_list, axis=1)
    img_output = transform.resize(img_output, [67, 455, 3])
    print(img_output.shape)
    io.imsave(path, img_output)
    # io.imshow(img_output)
    # io.show()


if __name__ == "__main__":
    id = ["113442", "114148","2404463"]
    save_img("./tmp.jpg", id)
