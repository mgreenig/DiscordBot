from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
from string import ascii_uppercase
from multiprocessing import Pool
import re
import pickle

# get the html data from a url
def get_html(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    html = bs(webpage, 'html.parser')
    return html

# get all club links under a url
def get_club_links(url):
    html = get_html(url)
    club_links = {elem.text: 'https://footballdatabase.com' + elem['href'] for elem in html.find_all('a', {'class': 'sm_logo-name clubbrowser-club'})}
    return club_links

# urls to club lists for all clubs starting with each letter
club_letter_urls = ['https://footballdatabase.com/clubs-list-letter/' + letter for letter in ascii_uppercase]

if __name__ == '__main__':

    pool = Pool(6)
    # get all club links for all club letter urls
    club_link_dicts = pool.imap(get_club_links, club_letter_urls)
    all_club_links = {}
    for club_link_dict in club_link_dicts:
        all_club_links.update(club_link_dict)
    for club in all_club_links:
        # add the lowercase name to the dictionary
        all_club_links[club.lower()] = all_club_links[club]
        # look for FC at the end or start of each club and add the name without FC
        if re.search('^FC\s+|\s+FC$', club):
            club_no_FC = re.sub('^FC\s+|\s+FC$', '', club)
            all_club_links[club_no_FC] = all_club_links[club]
            all_club_links[club_no_FC.lower()] = all_club_links[club]
    pool.close()
    pool.join()

    pickle.dump(all_club_links, open('club_links.p', 'wb'))