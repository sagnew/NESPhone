import requests
import re

from bs4 import BeautifulSoup


vgm_url = 'https://www.vgmusic.com/music/console/nintendo/nes/'
html_text = requests.get(vgm_url).text
soup = BeautifulSoup(html_text, 'html.parser')


def download_track(count, track_element):
    track_title = track_element.text.strip().replace('/', '-')
    download_url = '{}{}'.format(vgm_url, track_element['href'])
    file_name = '{} {}.mid'.format(count, track_title)

    r = requests.get(download_url, allow_redirects=True)
    open(file_name, 'wb').write(r.content)

    print('Downloaded: {}'.format(track_title, download_url))


if __name__ == '__main__':
    attrs = {
        'href': re.compile(r'\.mid$')
    }

    tracks = soup.find_all('a', attrs=attrs, string=re.compile(r'^((?!\().)*$'))

    count = 0
    for track in tracks:
        download_track(count, track)
        count += 1
    print(len(tracks))
