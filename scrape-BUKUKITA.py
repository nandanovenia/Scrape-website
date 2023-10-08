#https://dailydevsblog.com/troubleshoot/resolved-beautifulsoup-returns-none-when-using-find-for-an-element-118665/
'''library: openpyxl-3.0.10
'''
import pandas as pd
import requests 
from bs4 import BeautifulSoup


baseurl="http://www.bukabuku.com/"
headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33"}
produklink=[]
kode_category=["59","130"]
category_list=["orang-tua-keluarga","psikologi"]
categorylist=[]
for i in range(len(category_list)):
    for x in range(1,3):
        r = requests.get(f"http://www.bukabuku.com/browses/index/cid:{kode_category[i]}/c:{category_list[i]}/page:{x}/")
        soup = BeautifulSoup(r.content, "lxml")
        produklist = soup.find_all("span",class_="product_list_title")
        for item in produklist:
                for link in item.find_all('a',href=True):
                    produklink.append(baseurl + link["href"])
                    #category={"Kategori":category_list[i]}
                    categorylist.append(category_list[i])

booklist=[]
for link in produklink:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, "lxml")
    try:
        title=soup.find("span",class_="product_title").text.strip()
    except:
        title=""
    try:
        author=soup.find("a",class_="blue_link").text.strip()
    except:
        author=""

    try:
        price_original=soup.find("span",class_="price_discounted").text.strip()
    except:
        price_original=""

    try:
        price_discount=soup.find("span",class_="price").text.strip()
    except:
        price_discount=""

    try:
        desc=soup.find("div",class_="product_description").text.strip()
    except:
        desc=""

    book={
            "Judul":title,
            "Penulis":author,
            "Harga Asli":price_original,
            "Harga Diskon":price_discount,
            "Deskripsi":desc,
            "Link":link
        }
    booklist.append(book)   

#print(booklist)
df=pd.DataFrame(booklist)
df["Kategori"]=categorylist
print(booklist)

#df.to_excel("scrape_bukukita1.xlsx")