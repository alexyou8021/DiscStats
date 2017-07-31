from lxml import html
import requests
from bs4 import BeautifulSoup
import json
import xlwt
from xlwt import *
import sys

if len(sys.argv) == 4:
    tournament = sys.argv[1]
    teamid = sys.argv[2]
    password = sys.argv[3]
elif len(sys.argv) == 3:
    tournament = sys.argv[1] 
    teamid = sys.argv[2]
    password = ''
else:
    teamid = '5630483324993536'
    password = ''
    tournament = 'PBJ'

if password:
    post = requests.post('http://www.ultianalytics.com/rest/view/team/' + teamid + '/authenticate/' + password + '/')
    auth = post.headers['IUltimateAuth']
    page = requests.get('http://www.ultianalytics.com/rest/view/team/' + teamid + '/', headers={'IUltimateAuth':auth})
else:
    page = requests.get('http://www.ultianalytics.com/rest/view/team/' + teamid + '/')

soup = BeautifulSoup(page.content, 'html.parser')

team_info = json.loads(soup.text)
name = team_info['nameWithSeason']

if password:
    page = requests.get('http://www.ultianalytics.com/rest/view/team/' + teamid + '/games', headers={'IUltimateAuth':auth})
else:
    page = requests.get('http://www.ultianalytics.com/rest/view/team/' + teamid + '/games')
soup = BeautifulSoup(page.content, 'html.parser')

games = json.loads(soup.text)
gameids = []
for game in games:
    if game['tournamentName'] == tournament:
        print game['tournamentName'], game['opponentName']
        gameids.append(game['gameId'])

stat_url = 'http://www.ultianalytics.com/rest/view/team/' + teamid + '/stats/player'
if(gameids):
    stat_url += '?gameIds='
    for gameid in gameids:
        stat_url += gameid + "_"
stat_url = stat_url[:-1]

if password:
    page = requests.get(stat_url, headers={'IUltimateAuth':auth})
else:
    page = requests.get(stat_url)
soup = BeautifulSoup(page.content, 'html.parser')

team_stats = json.loads(soup.text)

book = xlwt.Workbook(encoding="utf=8")
sheet = book.add_sheet("Fantasy")
sheet.write(0, 0, '')
sheet.write(1, 0, 'Goals (5)')
sheet.write(2, 0, 'Assists (5)')
sheet.write(3, 0, 'D (4)')
sheet.write(4, 0, 'Callahan (20)')
sheet.write(5, 0, 'Turn (-4)')
sheet.write(6, 0, 'Throwing')
sheet.write(7, 0, 'Catches')
sheet.write(8, 0, 'D')
sheet.write(9, 0, 'Total')

sheet.write(24, 0, 'D-Points Played')
sheet.write(25, 0, 'D Efficiency')
sheet.write(26, 0, 'Completions')
sheet.write(27, 0, 'Passing %')
sheet.write(28, 0, 'Catches')
sheet.write(29, 0, 'Catching %')
sheet.write(30, 0, 'Throwaways')
sheet.write(31, 0, 'Drops')

# setting actual stats
scores = {}
team_stats = sorted(team_stats, key=lambda k: k['playerName'])
for x in range(0, len(team_stats)):
    if x < 25:
        letter = chr(x + ord('B'))
    else:
        letter = 'A' + str( chr(x - 26 + ord('B')))

    scores[team_stats[x]['playerName']] = letter

    sheet.write(0, x + 1, team_stats[x]['playerName'])
    sheet.write(1, x + 1, team_stats[x]['goals'])
    sheet.write(2, x + 1, team_stats[x]['assists'])
    sheet.write(3, x + 1, team_stats[x]['ds'])
    sheet.write(4, x + 1, team_stats[x]['callahans'])
    sheet.write(5, x + 1, Formula("SUM(" + letter + "31+" + letter + "32)"))
    sheet.write(6, x + 1, Formula("((" + letter + "28/100)*" + letter + "27)/2"))
    sheet.write(7, x + 1, Formula("((" + letter + "30/100)*" + letter + "29)/2"))
    sheet.write(8, x + 1, team_stats[x]['dpointsPlayed'])
    sheet.write(9, x + 1, Formula(letter + '2 * 5 + ' + letter + '3 * 5 + ' + letter + '4 * 4 + ' + letter + '5 * 20 + ' + "SUM($" + letter + "$7:$" + letter + "$9)"))

    sheet.write(24, x + 1, team_stats[x]['dpointsPlayed'])
    sheet.write(25, x + 1, team_stats[x]['drops'])
    sheet.write(26, x + 1, team_stats[x]['passes'])
    sheet.write(27, x + 1, team_stats[x]['passSuccess'])
    sheet.write(28, x + 1, team_stats[x]['catches'])
    sheet.write(29, x + 1, team_stats[x]['catchSuccess'])
    sheet.write(30, x + 1, team_stats[x]['throwaways'])
    sheet.write(31, x + 1, team_stats[x]['drops'])
    
file = open(team_info['name'] + "_teams.txt","r")
fteams = [line.rstrip('\n') for line in file]
teamno = 0
player_count = 0
captain = True
for fplayer in fteams:
    if fplayer == "":
        fletter = chr(2 + teamno + ord('A'))
        style = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour cyan_ega; borders: top thin, left thin, right thin, bottom thin")
        sheet.write(15 + player_count, 1 + teamno, 'Total', style)
        sheet.write(15 + player_count, 2 + teamno, Formula("SUM($" + fletter + "$15:$" + fletter + "$" + str(15 + player_count)  + ")"), style)
        teamno += 3 
        player_count = 0
        captain = True
        continue
    if captain:
        style = xlwt.easyxf("align: horiz center;")
        sheet.write_merge(13, 13, 1 + teamno, 2 + teamno, fplayer, style)
        style = xlwt.easyxf("pattern: pattern solid, fore_colour cyan_ega; borders: top thin, left thin, right thin, bottom thin")
        sheet.write(14, 1 + teamno, 'Players', style)
        sheet.write(14, 2 + teamno, 'Points', style)
        captain = False
        
    style = xlwt.easyxf("pattern: pattern solid, fore_colour cyan_ega; borders: left thin, right thin")
    sheet.write(15 + player_count, 1 + teamno, fplayer, style)
    sheet.write(15 + player_count, 2 + teamno, Formula(scores[fplayer] + '10'), style)
    player_count += 1

book.save(team_info['name'] + '.xls')
print 'New Excel File Saved.'
