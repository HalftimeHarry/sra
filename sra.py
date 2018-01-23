import sys
import requests
import sqlite3
import api_keys

'''
http://api.sportradar.us/football-t1/american/en/schedules/2018-01-14/results.json?api_key=6ps4fbsxgmqbapmcs687vsmz
'''
SPORTRADAR_URL = 'http://api.sportradar.us'
SPORT = 'football-t1/american'
LANGUAGE = 'en'
DATE = '2018-01-14'

class SportRadarAPI:
    def __init__(self):
        pass

    def clean_up(self):
        pass

    def get_db_name(self):
        return self.db

    def get_game_list(self, date):
        game_list = []
        cmd = SPORTRADAR_URL + '/' + SPORT + '/' + LANGUAGE + '/schedules/' + date + '/results.json?api_key=' + api_keys.FOOTBALL_API_KEY 
        print cmd
        r = requests.get(cmd)
        h = r.json()
        print h
        return game_list


if __name__ == '__main__':
    
    sra = SportRadarAPI()
    gl = sra.get_game_list('2018-01-14')
    sra.clean_up