import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor
from fpdf import FPDF


def download_slides(image_link, index):
    res = requests.get(image_link['data-full'])
    file_name = image_link['data-full'].split("/")[-1].split("?")[0]
    print(file_name)
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
    for index in range(1, len(images_links)+1):
        executor.submit(download_slides, images_links[index-1], index)


pdf = FPDF()
image_list = os.listdir()
for image in (sorted(image_list, key=lambda x: int(x.split("-")[2]))):
    pdf.add_page()
    pdf.image(image, 0, 0, 200, 200)
os.chdir("..")
pdf_name = link.split("/")[4].split("?")[0]
pdf.output(pdf_name+".pdf", "F")
