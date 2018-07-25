# -*- coding: utf-8 -*- 

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))




def test_get_Img_List():
    from lib.google_img_parser import get_Img_List
    test_keyword = '照片'
    img_list = get_Img_List(test_keyword)
    print len(img_list)
    pass

def test_download_page_by_list():
    from lib.google_img_parser import get_Img_List
    from lib.google_img_parser import download_page_by_list
    test_keyword = '照片'
    img_list = get_Img_List(test_keyword)
    download_page_by_list(img_list,'data')
    

    pass

    



if __name__  == "__main__":
    test_get_Img_List()
    test_download_page_by_list()