#This class is for get recruitment notice from https://rsj.sh.gov.cn/tzpgg_17408/index.html
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime
import sys
import os
# Ensure the project root is in sys.path so that sibling packages can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from db_helper.sqlitestorage import storage
import re

def random_delay(min_delay=1, max_delay=3):
    """随机延迟"""
    time.sleep(random.uniform(min_delay, max_delay))
    
def get_content(url:str):
    print(f'url is {url}')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers)

    # 解析HTML内容
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 提取数据
    title = soup.find('div', class_='TRS_Editor')
    contents = title.find_all('p')
    data =[]
    for content in contents:        
        data.append(content.text.strip())
    print(data)
    return ' '.join(data)

def clean_web_data(data_list):
    """
    清洗爬取的数据
    """
    cleaned_data = []
    
    for item in data_list:
        # 去除多余空白字符
        cleaned_item = {}
        for key, value in item.items():
            if isinstance(value, str):
                # 去除HTML标签
                clean_value = re.sub(r'<[^>]+>', '', value)
                # 去除多余空白
                clean_value = ' '.join(clean_value.split())
                cleaned_item[key] = clean_value
            else:
                cleaned_item[key] = value
        
        # 添加爬取时间
        cleaned_item['crawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cleaned_data.append(cleaned_item)
    
    return cleaned_data

# 发送HTTP请求
url = "https://rsj.sh.gov.cn/tzpgg_17408/index.html"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
response = requests.get(url, headers=headers)

# 解析HTML内容
soup = BeautifulSoup(response.content, 'html.parser')

# 提取数据
title = soup.find('ul', class_='uli14 nowrapli list-date no-margin-bottom')
articles = title.find_all('li')
# print(articles)

data = []
for article in articles:
    print( article.find('a'))
    random_delay()
    base_url = 'https://rsj.sh.gov.cn'
    page_url = article.find('a')['href']
    url = f'{base_url}{page_url}'
    item = {
        'title': article.find('a')['title'].strip(),
        'publish_date': article.find('span', class_='time').text.strip(),
        'url': url,
        'content':get_content(url),
        'crawl_timestamp': datetime.now(),
        'tags':'招聘公告'
    }
    storage.save_content(item)
    
    data.append(item)
print(data)
# 保存到DataFrame
df = pd.DataFrame(data)




        
    