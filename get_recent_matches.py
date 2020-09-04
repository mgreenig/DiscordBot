import pickle
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs

club_links = pickle.load(open('club_links.p', 'rb'))

# get the html data from a url
def get_html(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    html = bs(webpage, 'html.parser')
    return html

def get_recent_score(club):

    if club not in club_links:
        return 'Sorry we don\'t know that club'

    html = get_html(club_links[club])
    home_team = html.find('a', {'class': 'sm_logo-name limittext'})
    score = html.find('div', {'class': 'club-gamelist-match-score text-center'})
    away_team = html.find('a', {'class': 'sm_logo-name sm_logo-name_away'})
    return home_team.text + ' ' + score.text + ' ' + away_team.text