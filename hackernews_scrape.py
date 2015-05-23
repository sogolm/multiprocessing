from bs4 import BeautifulSoup
import requests
import json
from pymongo import MongoClient
from pymongo import Connection
from multiprocessing import Pool
from timeit import Timer
import threading
from requests import ConnectionError
from requests import TooManyRedirects


API_HOST = 'http://hckrnews.com/data/'
conn = MongoClient()
db = conn.hackernews
coll = db.hackerlinks


def get_metadata_for_dates_sequential(dates_path):
    """
    Scrapes posts meta data for a list of dates sequentially.
    """
    with open(dates_path) as f:
        dates = f.read().splitlines()
        for date in dates:
            get_date_metadata(date)



def get_date_metadata(date):
    """
    Function to scrape the posts meta data for one date in string format and dump into mongodb
    """
    url = API_HOST + date + ".js"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_posts = response.json()
            get_content_concurrent(json_posts)
            #coll.insert(json_posts_with_content)
    except (ConnectionError, TooManyRedirects), e:
        print e


def get_metadata_for_dates_multi(dates_path, pool_size=4):
    """
    Scrapes hackernews metadata for posts given a list of dates using the specified number of processes.
    """
    with open(dates_path) as f:
        dates = f.read().splitlines()
        pool = Pool(pool_size)
        pool.map(get_date_metadata, dates)
        pool.close()
        pool.join()


def get_articles_content(post_metadata):
    """
    Scrapes the content of a post given a single entry within mongodb
    """
    url = post_metadata[u'link']
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content)
            content_text = soup.get_text()
            post_metadata['content'] = content_text
            coll.insert(post_metadata)
    except (ConnectionError, TooManyRedirects), e:
        print e


def get_content_concurrent(json_metadata):
    """
    Scrape the content of each link within json response concurrently
    """
    threads = len(json_metadata)/4  # Number of threads to create
    jobs = []
    for i in range(0, threads):
        thread = threading.Thread(target=get_articles_content(json_metadata[i]))    #TODO: double check this
        jobs.append(thread)
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()


def main():
    t = Timer(lambda: get_metadata_for_dates_multi("data/dates"))
    print "Took %s seconds to scrape data using 4 cores." %t.timeit(number=1)
    db.drop_collection("hackerlinks")
    t = Timer(lambda: get_metadata_for_dates_sequential("data/dates"))
    print "Took %s seconds to scrape data using one process" %t.timeit(number=1)


if __name__ == '__main__':
    main()








