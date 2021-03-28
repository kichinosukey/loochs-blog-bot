import time
import datetime as dt

import requests
from bs4 import BeautifulSoup as bs4
import tweepy

from config import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, FILENAME


LINK_BLOG_ATAG_IDX = 7


def add_text(filename, str):
    with open(filename, mode='a') as f:
        f.write(str+'\n')

def check_date_existed(date_str):
    l = load_text(FILENAME)
    if date_str + '\n' in l:
        return True
    else:
        return False

def get_datestr_today(pattern):
    return dt.date.today().strftime(pattern)

def load_text(filename):
    with open(filename, mode='r') as f:
        return f.readlines()

def main(sleep_time):

    while check_date_existed(get_datestr_today('%Y/%m/%d')):
        print('%s is already posted.' % get_datestr_today('%Y/%m/%d'))
        time.sleep(sleep_time)

    date = get_datestr_today('%Y/%m/%d')

    url = 'https://loochs.org/' + date

    r = requests.get(url)

    if r.status_code == 200:

        # Auth
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        # Tweet content
        soup = bs4(r.text, 'html.parser')
        url = soup.find_all('a')[LINK_BLOG_ATAG_IDX].get('href')
        blog_title = soup.find('h2', {'class':'entry-title'}).text

        tweet = ''
        tweet += 'ブログ「' + blog_title + '」を更新しました！\n'
        tweet += url

        api.update_status(tweet)
        add_text(FILENAME, date+'\n')

if __name__ == '__main__':

    while True:

        main(10)
        time.sleep(10)