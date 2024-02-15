from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import requests
import random
import time

urls = ['https://thrivemyway.com/post-sitemap1.xml', 'https://www.siegemedia.com/post-sitemap.xml']


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Avast/121.0.0.0',
    'Accept': 'application/json',
}

current_date = datetime.now()
current_year = current_date.year
current_month = current_date.month
file_name = f'blogs_count_{current_month}-{current_year}'

rows = []
for url in urls:
    count = 0
    beauty_url = url.split('/')[2].replace('www.', '')
    new_row = {'Website': beauty_url, 'Count': None}

    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')

            lastmods = soup.find_all('lastmod')
            for lastmod in lastmods:

                date_obj = datetime.strptime(lastmod.text, "%Y-%m-%dT%H:%M:%S%z")
                if date_obj.year == current_year and date_obj.month == current_month:
                    count += 1

            actual_count = count - 1  # substract modifing pages "start-blog" from thrivemyway and "all" from siegemedia
            new_row['Count'] = int(actual_count)

        else:
            print(f"Failed to fetch data from {url}. Status code: {r.status_code}")
    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")

    rows.append(new_row)
    time.sleep(random.randint(1, 3))
    print(new_row)

df = pd.DataFrame(rows)
df.to_csv(f'data/{file_name}.csv', index=False)