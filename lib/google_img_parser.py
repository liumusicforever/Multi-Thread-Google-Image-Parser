import os
import json
import uuid

import urllib
import urllib2

from bs4 import BeautifulSoup

header={
'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'accept-language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,th;q=0.2',
'avail-dictionary':'8taZ3E7d',
'cache-control':'no-cache',
'cookie':'CGIC=IlV0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSxpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44; CONSENT=YES+TW.zh-TW+20170514-09-0; OGPC=19005936-2:19006818-1:; OGP=-19006818:; SID=RgZeyjsTap7noCBa6-amErEDdS2g-8Ja4yYKVdzuRet-l26ZKaU7pJk_zSgMHIDksx-LpQ.; HSID=AZ2ATb7pknyJtWOsF; SSID=As5xqYL43cr6p0wNU; APISID=0xmg1jP75ZpRzkfp/AfQV7aNNX5BjGaKhF; SAPISID=2rgqJOjtlvGsOxMQ/AroiWB5aX9Ifd0vst; NID=135=KBVr4FShfVofHPPNKKD8Zm83Q6T8b1CJGYdyanAMXrNFlgiD5v0P81KEg_MRAk4I7UESBXvtOCAjK-gx853_XAKIRV8jKVrL_mIiGIdQL6HwfEGzpz1esHQbjN43onZuFEdaUIBu6Gu8J9KyCtnqYm5bOB9DFZIKWg-31zCdOCbB-zODa4n0goKmPtyX-653o8Qr5Qp4Ho2SCI4uIvT4XWlW5bYV_4VDsCdf6_0CvI7gTQJNP4N1xez2OTXSrv0yVUgInqv5zwvXgL4wdO-tQoeUPZBNCSpC8IUXxnEkFyApIpEymfhBo8qlFHORJtkt8eYLValW7bSCmGE6jVfI1NaBL4_xDsdKfiWsscyhmAgYxRgthOsffV9g_dhECY4CjzzRAv46qqTtEbWWCyS5R0Cm8gQ_CH3Y0wfyF6rnnelk5IVq_Hw0P0dZbu54t1-5U9vSwr7CVImmpWwd9Mt3sgSmFtOtgHqRR68; GOOGLE_ABUSE_EXEMPTION=ID=93d5f67bd3951ae2:TM=1532427031:C=r:IP=118.167.117.138-:S=APGng0sEMJU3l-08yubMEL0r07U3MGqWUA; DV=YwGaG4qkT-USUHFnxQKTMX-fyli8TBY; 1P_JAR=2018-7-24-10; UULE=a+cm9sZToxIHByb2R1Y2VyOjEyIHByb3ZlbmFuY2U6NiB0aW1lc3RhbXA6MTUzMjQyNzEwMTI0MTAwMCBsYXRsbmd7bGF0aXR1ZGVfZTc6MjUwNDczNzQzIGxvbmdpdHVkZV9lNzoxMjE1MzkyNDE2fSByYWRpdXM6MTUzMjAyMA==',
'pragma':'no-cache',
'referer':'https://www.google.com.tw/',
'upgrade-insecure-requests':'1',
'user-agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
'x-client-data':'CIS2yQEIpLbJAQjEtskBCKmdygEI153KAQioo8oB'}

filtersize = 250

def get_img_by_url(url):
    try:
        req = urllib2.Request(url, headers=header)
        raw_img = urllib2.urlopen(req,timeout=20).read()
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


