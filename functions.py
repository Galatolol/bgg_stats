import time
from urllib.request import urlretrieve, urlopen
from xml.etree import ElementTree
from bs4 import BeautifulSoup

############################

def set_global_dates(min_date, max_date):
    global min_date_glob
    global max_date_glob
    min_date_glob = min_date
    max_date_glob = max_date

############################

def bold(string):
    return '\033[1m{0}\033[0m'.format(string)
    #return '**{0}**'.format(string)   # reddit bold
    #return '[b]{0}[/b]'.format(string)   # [b][/b] tags bold

############################

def get_xml_root(url):
    file = urlopen(url)
    return ElementTree.parse(file).getroot()

############################

def sort_by_plays(list):
    return sorted(list, key=lambda tup: tup[1], reverse=True)

############################

def print_tulpe_list(list)
    if len(list) == 0:
        return
    if len(list[0]) == 3:   # if a BGG ranking associated
        for index, item in enumerate(list):
            print('{:<3}. {:<80} {:>5} plays - BGG ranking: {:>3}'.format(index + 1, bold(item[0]), item[1], item[2]))
    else:
        for index, item in enumerate(list):
            print('{:>3}. {:<60} {:>3} plays'.format(index+1, bold(item[0]), item[1]))


    # if len(list[0]) == 3:
    #     print('No.|Game|Number of plays|BGG ranking\n---:|:---|---:|---:')
    #     for index, item in enumerate(list):
    #         print('{0}.|{1}|{2}|{3}'.format(index+1, bold(item[0]), item[1], item[2]))
    # else:
    #     print('No.|Game|Number of plays\n---:|:---|---:')
    #     for index, item in enumerate(list):
    #         print('{0}|{1}|{2}'.format(index+1, bold(item[0]), item[1]))   # reddit

############################

def print_plays(list, title):
    print('\n\n{0} plays from {1} to {2}\n'.format(bold(title), bold(min_date_glob), bold(max_date_glob)))
    print_tulpe_list(sort_by_plays(list))
    print('\nPlayed games: {0}/{1}'.format(bold(len([item for item in list if item[1] > 0])), bold(len(list))))
    print('All plays: {0}'.format(bold(sum([item[1] for item in list]))))

############################

def get_games_list_18xx():
    url_18xx = 'https://www.boardgamegeek.com/xmlapi2/family?id=19'
    list = get_xml_root(url_18xx).findall('./item/link')
    return [(item.attrib['id'], item.attrib['value']) for item in list if item.attrib['id'] not in open('18xx_extensions_id', 'r').read()]   # remove extensions from the list

############################

def get_games_list_top100():
    urlretrieve('http://boardgamegeek.com/browse/boardgame', filename='top100_html')
    with open('top100_html') as file_top100:
        soup = BeautifulSoup(file_top100, 'html.parser')
    soup_list = soup.findAll(attrs={'style' : 'z-index:1000;'})

    games_list = []
    for item in soup_list:
        games_list.append((item.contents[1].attrs['href'].split('/')[2], item.contents[1].contents[0], item.attrs['id'].replace('results_objectname', '')))

    return games_list

############################

def get_plays(list, top100=False):
    plays_list = []
    for item in list:
        game_id = item[0]
        game_name = item[1]
        url_plays = 'https://www.boardgamegeek.com/xmlapi2/plays?mindate={0}&maxdate={1}&id={2}'.format(min_date_glob, max_date_glob, game_id)

        print('Executing... Current game: {0}'.format(game_name))

        try:
            game_plays = int(get_xml_root(url_plays).attrib['total'])
        except ElementTree.ParseError:
            game_plays = 0

        if top100:
            plays_list.append((game_name, game_plays, item[2]))   # item[2] is a BGG ranking
        else:
            plays_list.append((game_name, game_plays))

        if len(plays_list) % 15 == 0:   # little break, so there aren't too many requests
            time.sleep(30)

    return plays_list

############################

def get_user_plays(username):
    url_user_plays = 'https://www.boardgamegeek.com/xmlapi2/plays?mindate={0}&maxdate={1}&username={2}'.format(min_date_glob, max_date_glob, username)
    user_plays = get_xml_root(url_user_plays)

    dictionary, user_plays_list = {}, []
    for child in user_plays:
        dictionary.setdefault(child[0].attrib['name'], []).append(child.attrib['quantity'])

    # sum all plays of the same game
    for item, item1 in dictionary.items():
        user_plays_list.append((item, sum(map(int, item1))))

    return user_plays_list