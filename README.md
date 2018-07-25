# Multi-Thread-Google-Image-Parser
The simple multi-thread parser for google image , and a small tool to remove duplicate image.

## Environment
* Python 2.7
* request
* BeautifulSoup


## How To Use
* Step 1 :
    type your header in `lib/google_img_parser.py` line 10 
    ```
    header={
    'accept':'',
    'accept-language':'',
    'avail-dictionary':'',
    'cache-control':'no-cache',
    'cookie':'',
    'pragma':'no-cache',
    'referer':'https://www.google.com.tw/',
    'upgrade-insecure-requests':'1',
    'user-agent':'',
    'x-client-data':''}
    ```
    **key:** You can open F12(develop mode) on Chrome and search keyword on google image , then open `Network -> Header` , get your own header
* Step 2 :
    Prepare your keywords , here is the `xxx_keywords.csv` format:
    ```
    1,<keyword 1 >
    2,<keyword 2 >
    3,<keyword 3 >
    4,<keyword 4 >
    ...
    ```
* Step 3 :
    Launch Parser
```shell
# arguments:
#   -h, --help            show this help message and exit
#   --csv_path CSV_PATH   the csv file path
#   --output_root OUTPUT_ROOT
#                         the output root

# example:
python Main.py --csv_path ./test.csv --output_root  ./data
```
* Step 4 :
    Find duplicate images and remove it , group images.
```shell
# optional arguments:
#   -h, --help            show this help message and exit
#   --clean_dataset CLEAN_DATASET
#                         the root of all cleaned datas
#   --mess_dataset MESS_DATASET
#                         the root of all mess datas
#   --group_num GROUP_NUM
#                         the number of each group

# example:

python find_duplicate.py --clean_dataset ./data1 --mess_dataset  ./data --group_num 2000
```
