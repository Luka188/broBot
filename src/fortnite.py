from src.Client import Client

def get_squad_stats(usernames, platform = 'psn'):

    if not isinstance(usernames, list):
        usernames = [usernames]

    client = Client()
    stats_friends = []
    try:
        for x in usernames:
            response = client.send_request(platform, x.lower())
            stats_friends.append(response[0]['p9'])
    except Exception:
        ''

    return stats_friends

def build_string_for_squad_stats(data):
    stats_friends = ''
    try:
        #stats_friends += '*'+x+'*\n'
        stats_friends += 'Played time: '+data[11]['displayValue']+'\n'
#        stats_friends += 'Top 1: '+data[0]['displayValue']+'\n'
 #       stats_friends += 'Top 3: '+data[1]['displayValue']+'\n'
  #      stats_friends += 'Top 5: '+data[2]['displayValue']+'\n'
   #     stats_friends += 'Top 10: '+data[4]['displayValue']+'\n'
        stats_friends += 'Win Ratio: '+data[8]['displayValue']+'\n'
        stats_friends += 'Kills: '+data[10]['displayValue']+'\n'
        stats_friends += 'Kills/Match: '+data[13]['displayValue']+'\n\n'
    except Exception as e:
        ''
    return stats_friends
