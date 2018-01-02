import json
import requests

class Client:

    URL = 'https://fortnitetracker.com/profile/'

    def send_request(self, platform, username):
        r = requests.get(self.URL + platform + '/' + username)
        response = r.text

        try:
            player_data = json.loads(self.find_between(response, 'var playerData = ', ';</script>'))
            account_info = json.loads(self.find_between(response, 'var accountInfo = ', ';</script>'))
            lifetime_stats = json.loads(self.find_between(response, 'var LifeTimeStats = ', ';</script>'))
        except Exception:
            return ''

        return [player_data, account_info, lifetime_stats]

    def find_between(self, s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""
