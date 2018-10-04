from requests_html import HTMLSession
from requests.exceptions import ConnectionError
import os
from tqdm import tqdm

# Create a session to get link
session = HTMLSession()

# Input for link album and quality , get all the links of song in album
print('CSNDownloader coded by JesseN!')
prompt ="Enter link album: "
while True:
    link_album = input(prompt)
    try:
        r = session.get(link_album)
        if r.status_code == 200:
            break
    except ConnectionError:
        print('Connection error, please try again later!')
prompt1 = input("Choose your quality(128,320,Loseless): ")
links = r.html.find('a[href$="_download.html"]')

# Create a list contains all the song names , remove duplicate link and put them in a list called result
song_names = []
result = []
for link in links:
    if 'title' in link.attrs:
        if link.attrs['title'].startswith('D'):
            song_names.append(link.attrs['title'][9:])
            result.append(''.join(list(link.absolute_links)))
formatted_text = 'Found {} songs'.format(len(result))
print(formatted_text)
print('Start downloading, please wait!')

# For each song links in the album contain 5 download links for 5 quality version, find all download links then store in a list
download_links = []
for song in result:
    try:
        r1 = session.get(song)
        if r1.status_code == 200:
            pass
    except ConnectionError:
        print('Connection error, please try again later!')
    download_link = r1.html.find('a[href*="downloads"]')
    for dl_link in download_link:
        download_links.append(''.join(list(dl_link.absolute_links)))

# Create a dict with key is song name and value is a list contains 5 download links for 5 quality version
a = [download_links[i:i+5] for i in range(0,len(download_links),5)]
d1 = dict(zip(song_names, a))

# Writing file in the parent folder contains the script
script_path = os.path.abspath(__file__)
parent_path = os.path.dirname(script_path)
chunk_size = 1024
for k,v in d1.items():
    k = k + '.mp3'
    if str(prompt1) == '128':
        try:
            r2 = session.get(v[0], stream=True)
            total_size = int(r2.headers['content-length'])
            if r2.status_code == 200:
                pass
        except ConnectionError:
            print('Connection error, please try again later')
    elif str(prompt1) == '320':
        try:
            r2 = session.get(v[1],stream=True)
            total_size = int(r2.headers['content-length'])
            if r2.status_code == 200:
                pass
        except ConnectionError:
            print('Connection error, please try again later')
    elif str(prompt1) == 'Loseless':
        try:
            r2 = session.get(v[3],stream=True)
            total_size = int(r2.headers['content-length'])
            if r2.status_code == 200:
                pass
        except ConnectionError:
            print('Connection error, please try again later')
    with open(os.path.join(parent_path, k),'wb') as f:
        for data in tqdm(iterable=r2.iter_content(chunk_size=chunk_size),total=round(total_size/chunk_size,4), unit='KB', desc='Downloading '+k):
            f.write(data)

print('Download complete, enjoy!')