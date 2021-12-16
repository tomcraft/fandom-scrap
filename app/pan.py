import requests, re
from bs4 import BeautifulSoup, Tag

def heat_soup(url, cache=[]):
    print("Scrapping page", url, "...")
    request = requests.get(url, allow_redirects=False)
    if request.status_code == 301 or request.status_code == 302:
        url_effective = request.headers['location']
        if url_effective in cache:
            return url_effective, None
        request = requests.get(url)
    else:
        url_effective = request.url
        if url_effective in cache:
            return url_effective, None
    
    htmlContent = request.content
    soup = BeautifulSoup(htmlContent, "lxml")
    print("  got page with title", soup.title.string)
    cache.append(url_effective)
    return url_effective, soup

def read_block_list():
    ignored_pages = ['https://minecraft.fandom.com/wiki/Stonecutter/old']
    blocks = []
    url, blockListPage = heat_soup("https://minecraft.fandom.com/wiki/Block")
    listHeader = blockListPage.find(attrs={'id': 'List_of_blocks'})
    listContent = listHeader.parent.find_next('ul')
    for entryContent in listContent:
        if isinstance(entryContent, Tag):
            tags = entryContent.find_all('a')
            pictureTag = tags[0]
            detailsTag = tags[1]
            url = 'https://minecraft.fandom.com' + detailsTag.attrs['href']
            if url in ignored_pages:
                continue
            blocks.append({
                    'id': 'minecraft:' + detailsTag.string.lower().replace(" ", "_").replace("-", "_"),
                    'name': detailsTag.string,
                    'image': pictureTag.attrs['href'],
                    'url': url
                })

    print("Found", len(blocks), "blocks")
    return blocks

def read_block_properties(url, cache_soup=[], cache_properties={}):
    properties = {}
    url_effective, page = heat_soup(url, cache_soup)
    if url_effective in cache_properties:
        return cache_properties[url_effective]
    table_body = page.find('div', class_='notaninfobox').find('table', class_='infobox-rows').tbody
    for table_entry in table_body.contents:
        if isinstance(table_entry, Tag):
            header = next(table_entry.th.stripped_strings).lower().replace(' ', '_').replace('-', '_')
            if header == 'tool' or header == 'tools':
                header = 'tools'
                data = []
                for tool in table_entry.td.find_all('a'):
                    data.append(tool.attrs['title'].lower())
                if len(data) == 0:
                    continue
            else:
                data = next(table_entry.td.stripped_strings).lower().replace('\u200c', '')
            if header == 'renewable':
                continue

            if header == 'stackable':
                header = 'stack_size'
                m = re.search(r'yes \((\d+)\)', data)
                if m:
                    data = m.group(1)
                else:
                    data = 1
            
            if header == 'flammable' and data != 'no':
                data = 'yes'
            
            if header == 'catches_fire_from':
                header = 'catches_fire_from_lava'
                if data != 'no':
                    data = 'yes'

            if data == '?':
                continue;

            if isinstance(data, str):
                if data.startswith('yes'):
                    data = 'yes'
                elif 'no' in data:
                    data = 'no'

            if isinstance(data, str):
                data = try_bool(data)
            if isinstance(data, str):
                data = try_integer(data.replace(',', ''))
            properties[header] = data
    cache_properties[url_effective] = properties
    return properties


def try_bool(str):
    if str == 'yes':
        return True
    elif str == 'no':
        return False
    else:
        return str

def try_integer(str):
    try:
        return int(str)
    except ValueError:
        return try_float(str)

    
def try_float(str):
    try:
        return float(str)
    except ValueError:
        return str