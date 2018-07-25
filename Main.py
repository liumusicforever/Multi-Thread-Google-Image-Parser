import os
import csv
import argparse
import Queue
from threading import Thread

from lib.google_img_parser import get_Img_List
from lib.google_img_parser import download_page_by_list


example_text = '''example:

python Main.py --csv_path ./test.csv --output_root  ./data

'''

#Main start mutiple threads to work effective
# create the instance
q = Queue.Queue()


    
parser = argparse.ArgumentParser( epilog=example_text,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('--csv_path', required=True, dest="csv_path", type=str, help="the csv file path")
parser.add_argument('--output_root', required=True, dest="output_root", type=str, help="the output root")
    

args = parser.parse_args()

csv_path = args.csv_path
output_root = args.output_root


def print_task():
    while not q.empty(): # check that the queue isn't empty
        each = q.get() # print the item from the queue
        print (each)
    
def do_task():
    while not q.empty(): # check that the queue isn't empty
        each = q.get() # print the item from the queue
        tesk_id = each[0]
        tesk_keyword = each[1]
        img_list = get_Img_List(tesk_keyword)

        out_dir = os.path.join(output_root,str(tesk_id))
        download_page_by_list(img_list,out_dir)



def main():

    # add items to the queue
    QueryList = csv.reader(open(csv_path))
    for i,each in enumerate(QueryList):
        q.put(each)

    for i in range(25): # aka number of threads
        t1 = Thread(target = do_task) # target is the above function
        t1.start() # start the thread

    q.join() # this works in tandom with q.task_done
            # essentially q.join() keeps count of the queue size
            # and q.done() lowers the count one the item is used
            # this also stops from anything after q.join() from
            # being actioned.

    
if __name__ == "__main__":
    main()