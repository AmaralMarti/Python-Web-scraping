from urllib.request import urlopen
from bs4 import BeautifulSoup
import queue
from threading import Thread
import time
import json

def convert_row_count(row_count):
    try:
        if row_count is not None:
            row_count = int(row_count.split(' ')[0].strip())
    except ValueError:
        row_count = None

    return row_count    

def convert_size(byte_count):
    items = byte_count.split(' ')

    size = float(items[0].strip())
    unit = items[1].strip()

    if unit == 'KB':
        size = size * 1000
    if unit == 'MB':
        size = size * 1000000
    
    return size

def get_file_details(text):
    items = text.strip().split('\n')

    for item in reversed(items):
        if item.strip() == '' or item.strip() == 'executable file':
            items.remove(item)

    row_count = None
    byte_count = None
    
    if len(items) == 1:
        byte_count = items[0].strip()
    elif len(items) == 2:
        row_count = items[0].strip()
        byte_count = items[1].strip()
    
    row_count = convert_row_count(row_count)
    byte_count = convert_size(byte_count)

    return row_count, byte_count

def openUr(url):
    count = 0
    html = None
    while count < 2000:
        try:
            html = urlopen(url)
            break
        except:
            count += 1
            print('contagem: ' + str(count))
            time.sleep(1)

    return html

def process_file(key, path):
    print('process_file - ' + path)
    # html = urlopen('https://github.com/' + path)
    html = openUr('https://github.com/' + path)
    bs = BeautifulSoup(html, 'lxml')
    
    text = bs.find('div', class_='text-mono').text
    row_count, byte_count = get_file_details(text)
    
    value = {         
        'path': path,
        'row_count': row_count,
        'byte_count': byte_count,
    }

    return key, value

def process_url(key, path):
    print('process_url  - ' + path)    
    # html = urlopen('https://github.com/' + path)
    html = openUr('https://github.com/' + path)
    bs = BeautifulSoup(html, 'lxml')
    
    grid = bs.find('div', class_='js-details-container Details')

    items = grid.find_all('div', role='row', class_='Box-row')

    que = queue.Queue()
    threads_list = list()        

    output = dict()
    for item in items:
        svg = item.find('svg')

        if svg is None:
            continue

        item_type = svg['aria-label']
    
        a = item.find('a')
        name = a['title']
        item_path = a['href']
        
        if item_type == 'Directory':
            t = Thread(target=lambda q, arg1: q.put(process_url(name, arg1)), args=(que, item_path))
            # output[name] = process_url(item_path)
            
        if item_type == 'File':
            t = Thread(target=lambda q, arg1: q.put(process_file(name, arg1)), args=(que, item_path))

        t.start()
        threads_list.append(t)            

    for t in threads_list:
        t.join()
   
    while not que.empty():
        key, value = que.get()
        output[key] = value

    return key, output

_, tree = process_url('.', 'freeCodeCamp/freeCodeCamp')
#tree = process_url('vivadecora/desafio-backend-trabalhe-conosco')
#tree = process_url('ohmyzsh/ohmyzsh')
print(json.dumps(tree, indent = 2))