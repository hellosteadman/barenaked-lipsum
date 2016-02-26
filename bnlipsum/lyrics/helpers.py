from pyquery import PyQuery as P
from urlparse import urljoin
import requests
import re


def get_albums(artist_url):
    response = requests.get(
        artist_url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) '
                          'AppleWebKit/537.75.14 (KHTML, like Gecko) '
                          'Version/7.0.3 Safari/7046A194A'
        }
    )

    page = P(response.content)

    for album in page('div.album'):
        text = album.text_content()
        match = re.search(r'(?:album|compilation): "(.+)" \((\d+)\)', text)

        if match is None:
            continue

        album_title, album_year = match.groups()
        tracks = []

        for sibling in album.itersiblings():
            if sibling.tag == 'a':
                track_url = sibling.get('href')
                track_title = sibling.text_content()

                if not track_title or not track_url:
                    continue

                tracks.append(
                    (
                        track_title,
                        urljoin(artist_url, track_url)
                    )
                )

                pass
            elif sibling.tag == 'div' and sibling.get('class') == 'album':
                break

        yield album_title, album_year, tracks


def get_lyrics(track_url):
    response = requests.get(
        track_url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) '
                          'AppleWebKit/537.75.14 (KHTML, like Gecko) '
                          'Version/7.0.3 Safari/7046A194A'
        }
    )

    page = P(response.content)
    lyrics_container = page.find('div .text-center div').not_('[class]')

    if lyrics_container is not None:
        lines = lyrics_container.html().replace('<br/>', '\n').splitlines()
        sections = []
        section = ''
        chorus = False

        for line in lines:
            if line.startswith('<!--') or line.strip() == '&#13;':
                continue

            if line.strip() == '<i>[Chorus]</i>':
                continue

            if line.strip() == '<i>[Chorus:]</i>':
                chorus = True
                continue

            if line.strip().startswith('<'):
                continue

            if not line.strip():
                if section:
                    sections.append(
                        (section.strip(), chorus)
                    )

                    section = ''
                    chorus = False

                continue

            section += line.strip() + '\n'

        if section:
            sections.append(
                (section.strip(), chorus)
            )

        return sections
