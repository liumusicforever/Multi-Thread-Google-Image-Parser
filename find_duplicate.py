import os
import hashlib
import shutil
import uuid
import argparse

example_text = '''example:

python find_duplicate.py --clean_dataset ./data1 --mess_dataset  ./data --group_num 2000

'''

parser = argparse.ArgumentParser( epilog=example_text,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('--clean_dataset', required=True, dest="clean_dataset", type=str, help="the root of all cleaned datas")
parser.add_argument('--mess_dataset', required=True, dest="mess_dataset", type=str, help="the root of all mess datas")
parser.add_argument('--group_num', required=True, dest="group_num", type=int, help="the number of each group")
    

args = parser.parse_args()

clean_dataset = args.clean_dataset
mess_dataset = args.mess_dataset

def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_img_list(work_path):
    image_list = []
    otherfile_list = []
    db_path_list = []
    for root , subdir , files in os.walk(work_path):
        for each_file in files:
            if 'jpg' in each_file:
                image_path = root+'/'+each_file
                image_list.append([each_file,image_path])
            else:
                odr_path = root+'/'+each_file
                otherfile_list.append(odr_path)
    return image_list


def find_duplicate(img_list , dataset = {}):
    dup_list = list(list())
    cln_list = list(list())
    total_img_count = len(img_list)
    for i,(filename,img_path) in enumerate(img_list):
        #print file_name
        hash_code = hashlib.sha512(open(img_path,'rb').read()).hexdigest()
        #print hash_code
        if dataset.get(hash_code):
            dup_list.append([filename,img_path])
        else:
            cln_list.append([filename.split('.')[0],img_path])
        dataset.update({hash_code:img_path})
        if i%1000 ==0:
            print 'current finish {} img parsing'.format(i)
            print 'duplicate : ',len(dup_list)
            print 'total size : ',total_img_count
    return dup_list,cln_list


def get_dataset(img_list):
    dataset = dict()
    total_img_count = len(img_list)
    dataset.update({'hash_code':'img_path'})
    for i,(filename,img_path) in enumerate(img_list):
        hash_code = hashlib.sha512(open(img_path,'rb').read()).hexdigest()
        dataset.update({hash_code:img_path})
        if i % 1000 == 0:
            print 'current : {} total size : {}'.format(i,total_img_count)
    return dataset


def main():
    assert (clean_dataset != mess_dataset)
    img_list_cln = get_img_list(clean_dataset)
    img_list_blk = get_img_list(mess_dataset)

    dataset = get_dataset(img_list_cln)
    
    dup_list,cln_list = find_duplicate(img_list_blk,dataset)
    print 'duplicate : ',len(dup_list)
    print 'cln_list : ',len(cln_list)
    print 'total size : ',len(img_list_blk)


    print ('remove duplicate')
    for i,(filename,img_path) in enumerate(dup_list):
        os.remove(img_path)
    
    mkdirs(clean_dataset)
    if len(os.listdir(clean_dataset)) > 0:
        group_id = max([int(i.replace('g_','')) for i in os.listdir(clean_dataset)])
    else:
        group_id = 0
        
    
    for i,(filename,img_path) in enumerate(cln_list):
        if i % 3 == 0:
            group_id += 1
        out_dir = os.path.join(clean_dataset,'g_{}'.format(group_id))
        mkdirs(out_dir)
        img_name = str(uuid.uuid4()) + '.jpg'
        shutil.move(img_path,os.path.join(out_dir,img_name))
        
        


if __name__ == "__main__":
    main()