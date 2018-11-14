import datetime
from functions import print_plays, get_plays, get_games_list_top100, get_games_list_18xx, get_user_plays, set_global_dates, print_amateur_publishers

min_date = str(datetime.date.today() - datetime.timedelta(days=31))   # current date minus 30 days
max_date = str(datetime.date.today())
#min_date = '2017-08-01'
#max_date = '2017-08-31'
set_global_dates(min_date, max_date)

#print_plays(get_plays(get_games_list_top100(), True), 'TOP 100')
#print_plays(get_plays(get_games_list_18xx()), '18xx')

#username = 'Galatolol'
#print_plays(get_user_plays(username), username)

print_amateur_publishers(get_games_list_18xx())










