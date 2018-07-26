import os
import json
import uuid

import urllib
import urllib2

from bs4 import BeautifulSoup

header={
'accept':'',
'accept-language':'',
'avail-dictionary':'8taZ3E7d',
'cache-control':'no-cache',
'cookie':'',
'pragma':'no-cache',
'referer':'https://www.google.com.tw/',
'upgrade-insecure-requests':'1',
'user-agent':'',
'x-client-data':''}

filtersize = 200000

def get_img_by_url(url):
    try:
        req = urllib2.Request(url, headers=header)
        raw_img = urllib2.urlopen(req,timeout=30).read()
        filesize = raw_img.__sizeof__()
        return filesize , raw_img

    except Exception as e:
        print (e)
        return False , e


def get_Img_List(keyword):
    keyword= urllib.quote(keyword)
    keyword= keyword.split()
    keyword='+'.join(keyword)
    #hl=zh-TW&
    url="https://www.google.com.tw/search?q="+keyword+"&authuser=0&site=imghp&tbm=isch&source=lnms&biw=2133&bih=1055"
    soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')
    # contains the imgURL for Large original images, type of  image
    images_list=[]
    for web in soup.find_all("div",{"class":"rg_meta"}):
        imgURL , Type =json.loads(web.text)["ou"]  ,json.loads(web.text)["ity"]
        images_list.append((imgURL,Type))
    return images_list


def download_page_by_list(img_list,output_dir):
    image_type = 'img'
    mkdirs(output_dir)
    imt_path_list = []
    for i , (imgURL , Type) in enumerate( img_list):
        # check if jpg
        if Type != 'jpg':
            continue
        # get raw data
        fsize , fraw = get_img_by_url(imgURL)
        # check have response data
        if not fsize:
            continue
        # filter size of file too small
        if fsize > filtersize:
            
            filename = str(uuid.uuid4())
            filepath = os.path.join(output_dir,filename + '.' + Type)
            f = open(filepath, 'wb')
            f.write(fraw)
            f.close()
            imt_path_list.append(filepath)
    return imt_path_list
        
            
                

def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


