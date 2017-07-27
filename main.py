import datetime
from functions import print_top100_plays, print_18xx_plays, get_plays, get_games_list_top100, get_games_list_18xx

min_date = str(datetime.date.today() - datetime.timedelta(days=30))   # current date minus 30 days

print_top100_plays(get_plays(get_games_list_top100(), min_date, True))
print_18xx_plays(get_plays(get_games_list_18xx(), min_date))










