import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor


def download_slides(image_link):
    image_link = image_link.split("?")[0]
    res = requests.get(image_link.split("?")[0])
    file_name = image_link.split("/")[-1].split("?")[0]

    with open(file_name, 'wb') as image_file:
        image_file.write(res.content)


link = input("Enter url of the page: ")
# link = "https://www.slideshare.net/MohamedTalaat9/digital-watermarking-91878439?qid=3c79fb40-c68e-468f-bc6e-fde768d5fb2e&v=&b=&from_search=9"

folder_path = link.split("/")[4].split("?")[0]
if not os.path.exists(folder_path):
    os.mkdir(folder_path)
os.chdir(folder_path)
res = requests.get(link)
soup = BeautifulSoup(res.text, 'lxml')
images_links = soup.select('#slide-container')
print(type(images_links))
urls = images_links[0].find_all('source')


with ThreadPoolExecutor(max_workers=5) as executor:
    for url in urls:
        image_url = (url.get("srcset").split()[-2])
        executor.submit(download_slides, image_url)
