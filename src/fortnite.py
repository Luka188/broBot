from src.Client import Client
from prettytable import *

def get_stats(usernames, playlist, platform = 'pc'):

    if not isinstance(usernames, list):
        usernames = [usernames]

    client = Client()
    stats_friends = []
    try:
        for x in usernames:
            response = client.send_request(platform, x.lower())
            stats_friends.append(response[0][playlist])
    except Exception as e:
        print(e)
    return stats_friends

def build_string_for_stats(username, data):
    stats_friends = ''
    try:
        #stats_friends += '*'+x+'*\n'
        stats_friends += 'Fortnite Stats for ' + username + ':\n\n'
        stats_friends += 'Top 1: '+data[2]['displayValue']+'\n'
        stats_friends += 'Top 5: '+data[3]['displayValue']+'\n'
        stats_friends += 'Top 10: '+data[5]['displayValue']+'\n'
        stats_friends += 'K/D: '+data[8]['displayValue']+'\n'
        stats_friends += 'Matches: '+data[10]['displayValue']+'\n'
        stats_friends += 'Win %: '+data[5]['displayValue']+'\n'
        stats_friends += 'Score per match: '+data[16]['displayValue']+'\n'
    except Exception as e:
        ''
    return stats_friends

def get_all_stats(usernames, platform = 'pc'):
    all_stats = []
    playlist = ['p2','p10','p9']

    if not isinstance(usernames, list):
        usernames = [usernames]
    client = Client()
    stats_friends = []
    try:
        for i in range(3):
            for x in usernames:
                response = client.send_request(platform, x.lower())
                all_stats.append(response[0][playlist[i]])
    except Exception:
        ''
    return all_stats

def build_string_for_all_stats(username, data):
    try:
        t = PrettyTable([username, 'Solos', 'Duos', 'Squads'])
        t.add_row(['Top 1:', data[0][2]['displayValue'], data[1][2]['displayValue'], data[2][2]['displayValue']])
        t.add_row(['Top 5:', data[0][3]['displayValue'], data[1][3]['displayValue'], data[2][3]['displayValue']])
        t.add_row(['Top 10:', data[0][3]['displayValue'], data[1][3]['displayValue'], data[2][3]['displayValue']])
        t.add_row(['K/D:', data[0][8]['displayValue'], data[1][8]['displayValue'], data[2][8]['displayValue']])
        t.add_row(['Matches:', data[0][10]['displayValue'], data[1][10]['displayValue'], data[2][10]['displayValue']])
        t.add_row(['Win %:', data[0][9]['displayValue'], data[1][9]['displayValue'], data[2][9]['displayValue']])
        t.add_row(['Score per match:', data[0][16]['displayValue'], data[1][16]['displayValue'], data[2][16]['displayValue']])
        return t
        '''
        stats_friends += 'Fortnite Stats for ' + username + ':\n\n'
        stats_friends += 'Top 1: '+data[0]['displayValue']+'\n'
        stats_friends += 'Top 3: '+data[1]['displayValue']+'\n'
        stats_friends += 'Top 5: '+data[2]['displayValue']+'\n'
        stats_friends += 'Top 6: '+data[3]['displayValue']+'\n'
        stats_friends += 'Top 10: '+data[4]['displayValue']+'\n'
        stats_friends += 'Top 12: '+data[5]['displayValue']+'\n'
        stats_friends += 'Top 25: '+data[6]['displayValue']+'\n'
        stats_friends += 'Win %: '+data[8]['displayValue']+'\n'
        stats_friends += 'Matches: '+data[9]['displayValue']+'\n'        
        stats_friends += 'Played time: '+data[11]['displayValue']+'\n'
        stats_friends += 'K/d: '+data[7]['displayValue']+'\n'
        stats_friends += 'Avg. Kills/Match: '+data[13]['displayValue']+'\n'
        stats_friends += 'Total Kills: '+data[10]['displayValue']+'\n\n'
        '''
    except Exception as e:
        print(e)
