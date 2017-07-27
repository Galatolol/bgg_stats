import time
from urllib.request import urlretrieve, urlopen
from xml.etree import ElementTree
from bs4 import BeautifulSoup

def bold(string):
    return '\033[1m' + string + '\033[0m'

def parse_xml(url):
    file = urlopen(url)
    return ElementTree.parse(file).getroot()

def sort_by_plays(list):
    return sorted(list, key=lambda tup: tup[1], reverse=True)

def print_tulpe_list(list, top100=False):
    for index, item in enumerate(list):
        if top100:
            print('{:>3}. {:<80} {:>5} plays - BGG ranking: {:>3}'.format(index + 1, bold(item[0]), item[1], item[2]))
        else:
            print('{:>3}. {:<55} {:>3} plays'.format(index + 1, bold(item[0]), item[1]))

def print_top100_plays(list):
    print('\n\n{0}\n'.format(bold('TOP 100')))
    print_tulpe_list(list, top100=True)
    print('\n\n')
    print_plays(list, top100=True)

def print_18xx_plays(list):
    print('\n\n{0}\n'.format(bold('18xx')))
    print_plays(list)

def print_plays(list, top100=False):
    print_tulpe_list(sort_by_plays(list), top100)
    print('\nPlayed games: {0}/{1}'.format(len([item for item in list if item[1] > 0]), len(list)))
    print('All plays: {0}'.format(sum([item[1] for item in list])))

############################

def get_games_list_18xx():
    url_18xx = 'https://www.boardgamegeek.com/xmlapi2/family?id=19'
    list = parse_xml(url_18xx).findall('./item/link')
    return [(item.attrib['id'], item.attrib['value']) for item in list if item.attrib['id'] not in open('18xx_extensions_id', 'r').read()]   # remove extensions from the list

def get_games_list_top100():
    urlretrieve('http://boardgamegeek.com/browse/boardgame', filename='top100_html')
    with open('top100_html') as file_top100:
        soup = BeautifulSoup(file_top100, 'html.parser')
    soup_list = soup.findAll(attrs={'style' : 'z-index:1000;'})

    list = []
    for item in soup_list:
        list.append((item.contents[1].attrs['href'].split('/')[2], item.contents[1].contents[0], item.attrs['id'].replace('results_objectname', '')))

    return list

def get_plays(list, min_date, top100=False):
    plays_list = []
    for item in list:
        game_id = item[0]
        game_name = item[1]

        url_plays = 'https://www.boardgamegeek.com/xmlapi2/plays?' + 'mindate=' + min_date + '&id=' + game_id
        game_plays = int(parse_xml(url_plays).attrib['total'])

        if top100:
            plays_list.append((game_name, game_plays, item[2]))
        else:
            plays_list.append((game_name, game_plays))
        print('Executing... Current game: {0}'.format(game_name))

        if len(plays_list) % 15 == 0:   # little break, so there aren't too many requests
            time.sleep(30)

    return plays_list