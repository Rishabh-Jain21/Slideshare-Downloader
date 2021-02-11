import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor


def download_slides(image_link):
    res = requests.get(image_link['data-full'])
    file_name = image_link['data-full'].split("?")[0].split("/")[-1]
    with open(file_name, 'wb') as image_file:
        image_file.write(res.content)


link = input("Enter url of the page: ")
#link = "https://www.slideshare.net/MohamedTalaat9/digital-watermarking-91878439?qid=3c79fb40-c68e-468f-bc6e-fde768d5fb2e&v=&b=&from_search=9"


if not os.path.exists(link.split("/")[4].split("?")[0]):
    os.mkdir(link.split("/")[4].split("?")[0])
os.chdir(link.split("/")[4].split("?")[0])
res = requests.get(link)
soup = BeautifulSoup(res.text, 'lxml')
images_links = soup.select('.slide_image')

with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(download_slides, images_links)
