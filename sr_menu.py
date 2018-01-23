import cmd
import pickle
import time
import sys
import os
import sql

DD_VERSION = '0.8'

class game_menu(cmd.Cmd):
    
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = " game ->"
        self.game_interactive_menu()

    def game_interactive_menu(self):
        
        print "\n ---[ Football Atom Smasher - Version: " + DD_VERSION + " ]---\n\n" + \
        " Away team: %s" % (s.away_team) + "\n"\
        " Home team: %s" % (s.home_team) + "\n"\
        " Start date: %s" % (s.start_date) + "\n"\
        " End date: %s" % (s.end_date) + "\n"\
        " Number of prior games: %s" % (s.number_of_prior_games) + "\n\n"\
        " 1). Set home team\n" + \
        " 2). Set date range\n" + \
        " 3). Set number of prior games\n" + \
        " 4). Get average total of prior games between date range\n" + \
        " 5). Get Vegas total and set prediction\n" + \
        " 6). Get games from home team between date range\n" + \
        " 7). Get last number of games from home team\n" + \
        " 8). Get OU total\n" + \
        " 9). Targeted game details\n" + \
        "10). All game details\n" + \
        "11). Get home teams for season, week\n" + \
        '   Select a number to choose an item or "Q" to quit.\n'
    
    #--------------------------------------
    # Set home team
    #--------------------------------------
    def do_1(self, line):
        s.set_home_team()
        self.game_interactive_menu()
        
    #--------------------------------------
    # Set start date
    #--------------------------------------
    def do_2(self, line):
        s.set_date_range()
        self.game_interactive_menu()
        
    #--------------------------------------
    # Set number of prior games
    #--------------------------------------
    def do_3(self, line):
        s.set_number_of_prior_games()
        self.game_interactive_menu()
        
    #--------------------------------------
    # Get average total of prior games within date range   
    #--------------------------------------
    def do_4(self, line):
        average_game_score = s.get_average_total_of_prior_games_within_date_range(s.home_team, s.start_date, s.end_date)
        print "Average game score:", average_game_score
        self.game_interactive_menu()
        
    #--------------------------------------
    # Get Vegas total and set prediction 
    #--------------------------------------
    def do_5(self, line):
        game_list = s.get_teams_scores_ou_total_within_time_range(s.start_date, s.end_date)
        for g in game_list:
            print g
        self.game_interactive_menu()
        
    #--------------------------------------
    # Get games from home team   
    #--------------------------------------
    '''Get games from home team'''
    def do_6(self, line):
        home_game_list = s.get_games_from_home_team_between_date_range(s.home_team, s.start_date, s.end_date)
        for g in home_game_list:
            print g
        self.game_interactive_menu()
    
    #--------------------------------------
    # Get last X games from home team within date range  
    #--------------------------------------
    '''Get last X games from home team within date range'''
    def do_7(self, line):
        home_game_list = s.get_last_number_of_games_from_home_team_within_date_range(s.home_team, s.start_date, s.end_date)
        for g in home_game_list:
            print g
        self.game_interactive_menu()


    #--------------------------------------
    # Get OU Total
    #--------------------------------------
    def do_8(self, line):

        ou_total = s.get_closing_ou_total(s.home_team, s.end_date)
        print "OU total:", ou_total
        self.game_interactive_menu()

    
    #--------------------------------------
    # Get Targeted game details
    #--------------------------------------
    def do_9(self, line):

        targeted_game = s.get_targeted_game_details(s.home_team, s.start_date, s.end_date)
        print "Targeted game:", targeted_game
        self.game_interactive_menu()


    #--------------------------------------
    # Get Targeted game details
    #--------------------------------------
    def do_10(self, line):

        season = raw_input(" Enter season: ")
        week = raw_input(" Enter week: ")
        end_date = raw_input(" Enter end date: ")
        home_team_list = s.get_home_team_list_for_season_week(season, week, end_date)

        for home_team in home_team_list:
            targeted_game = s.get_targeted_game_details(home_team, s.start_date, end_date)
            print "Targeted game:", targeted_game
        self.game_interactive_menu()


    #--------------------------------------
    # Get home teams for season, week 
    #--------------------------------------
    def do_11(self, line):
        season = raw_input(" Enter season: ")
        week = raw_input(" Enter week: ")
        end_date = raw_input(" Enter end date: ")
        home_team_list = s.get_home_team_list_for_season_week(season, week, end_date)
        for g in home_team_list:
            print g
        self.game_interactive_menu()

    #--------------------------------------
    # Run
    #--------------------------------------
    def do_run(self, line):
        s.run()
        self.game_interactive_menu()
        
    def help_run(self, line):
        print "Computes the best over/under odds."
    def help_quit(self, line):
        print "Quit saves configuration data and returns to the main menu\n"
    def do_quit(self, line):
        return True

        # shortcuts for single letter commands

    help_r = help_run
    help_q = help_quit
    help_e = help_quit
    do_q = do_quit
    do_e = do_quit
    do_r = do_run



class confVars():
    
    def loadVars(self):
        global cfgFilename
        global conf
        global numVers
        global numThreads
        global loTestFileSz
        global hiTestFileSz
        global loKeySz
        global hiKeySz
        global numLoops
        global debuglevel

        cfgFilename = "gameConf.pkl"
        
        try:
            fin = open(cfgFilename, 'rb')
        
        except IOError:
            conf = {'numVers': '10',
                    'numThreads': '100',
                    'loTestFileSz': '100',
                    'hiTestFileSz': '1000000',
                    'loKeySz': '3',
                    'hiKeySz': '32',
                    'numLoops': '10',
                    'debuglevel': 'MED'}
            selfref_list = [1, 2, 3, 4, 5, 6, 7]
            selfref_list.append(selfref_list)
            fout = open(cfgFilename, 'wb')
            pickle.dump(conf, fout)
            pickle.dump(selfref_list, fout, -1)
            fout.close()
            fin = open(cfgFilename, 'rb')
        
        finally:                   
            conf = pickle.load(fin)
            fin.close()
            numVers = conf['numVers']
            numThreads = conf['numThreads']
            loTestFileSz = conf['loTestFileSz']
            hiTestFileSz = conf['hiTestFileSz']
            loKeySz = conf['loKeySz']
            hiKeySz = conf['hiKeySz']
            numLoops = conf['numLoops']
            debuglevel = conf['debuglevel']

    def getAll(self):
        global conf
        self.loadVars()
        return conf

    def getVar(self, varName):
        global conf
        self.loadVars()
        return conf[varName]
    
    def setVar(self, varName, value):
        global numVers
        global numThreads
        global loTestFileSz
        global hiTestFileSz
        global loKeySz
        global hiKeySz
        global numLoops
        global debuglevel

        self.loadVars()
        if varName == 'numVers':
            numVers = value
        elif varName == 'numThreads':
            numThreads = value
        elif varName == 'loTestFileSz':
            loTestFileSz = value
        elif varName == 'hiTestFileSz':
            hiTestFileSz = value
        elif varName == 'loKeySz':
            loKeySz = value
        elif varName == 'hiKeySz':
            hiKeySz = value
        elif varName == 'numLoops':
            numLoops = value
        elif varName == 'debuglevel':
            debuglevel = value
        self.saveVars()

    def saveVars(self):
        global numVers
        global numThreads
        global loTestFileSz
        global hiTestFileSz
        global loKeySz
        global hiKeySz
        global numLoops
        global debuglevel

        conf = {'numVers': numVers,
                'numThreads': numThreads,
                'loTestFileSz': loTestFileSz,
                'hiTestFileSz': hiTestFileSz,
                'loKeySz': loKeySz,
                'hiKeySz': hiKeySz,
                'numLoops': numLoops,
                'debuglevel': debuglevel}
                
        selfref_list = [1, 2, 3, 4, 5, 6, 7]
        selfref_list.append(selfref_list)
        fout = open(cfgFilename, 'wb')
        pickle.dump(conf, fout)
        pickle.dump(selfref_list, fout, -1)
        fout.close()



if __name__ == '__main__':
    
    s = sql.Sql('games.db')
    game_menu().cmdloop(' Enter a command:') 
