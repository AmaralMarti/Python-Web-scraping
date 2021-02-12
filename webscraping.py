from urllib.request import urlopen
from bs4 import BeautifulSoup
import queue
from threading import Thread
import time

def convert_row_count(row_count):
    try:
        row_count = int(row_count.split(' ')[0].strip())
    except ValueError:
        row_count = 0

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

    row_count = ''
    byte_count = ''
    
    if len(items) == 1:
        byte_count = items[0].strip()
    elif len(items) == 2:
        row_count = items[0].strip()
        byte_count = items[1].strip()
    
    row_count = convert_row_count(row_count)
    byte_count = convert_size(byte_count)

    return row_count, byte_count

def process_file(path):
    print('process_file - ' + path)
    html = urlopen('https://github.com/' + path)
    bs = BeautifulSoup(html, 'lxml')
    
    text = bs.find('div', class_='text-mono').text
    row_count, byte_count = get_file_details(text)
    
    value = {         
        'path': path,
        'row_count': row_count,
        'byte_count': byte_count,
    }

    return value

def process_url(path):
    print('process_url  - ' + path)    
    html = urlopen('https://github.com/' + path)

    bs = BeautifulSoup(html, 'lxml')
    
    grid = bs.find('div', class_='js-details-container Details')

    items = grid.find_all('div', role='row', class_='Box-row')

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
            output[name] = process_url(item_path)
            
        if item_type == 'File':
            output[name] = process_file(item_path)

    return output
