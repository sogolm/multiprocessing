from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
from multiprocessing import Pool
from timeit import Timer
import threading


API_HOST = 'http://hckrnews.com/data/'
conn = MongoClient()
db = conn.hackernews
coll = db.hackerposts


class MultiScraper():
    """
    Uses the hackernews api to scrape everyday posts meta data using multiple
    processes and download each day's posts' content using multiple threads.
    """
    def __init__(self, client, mongodb_name, collection_name, pool_size=4):
        self.client = client
        self.db = self.client[mongodb_name]
        if collection_name in self.db.collection_names():
            self.db[collection_name].drop()
        self.coll = self.db[collection_name]
        self.pool_size = pool_size

    def get_date_metadata(self, date):
        """
        Function to scrape the posts meta data for one date in string format.
        """
        url = API_HOST + date + ".js"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                json_posts = response.json()
                self.get_content_concurrent(json_posts)
        except (requests.ConnectionError, requests.TooManyRedirects, requests.Timeout), e:
            print e

    def get_metadata(self, dates_path):
        """
        Scrapes hackernews metadata for posts given a list of dates using the specified number of processes.
        """
        with open(dates_path) as f:
            dates = f.read().splitlines()

            # Create a multiprocessing pool.
            pool = Pool(self.pool_size)
            pool.map(self.get_date_metadata, dates)
            pool.close()
            pool.join()

    def get_post_content(self, post_metadata):
        """
        Scrapes the content of a post given a single entry in json
        """
        url = post_metadata[u'link']
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content)
                content_text = soup.get_text()
                post_metadata['content'] = content_text
                coll.insert(post_metadata)
        except (requests.ConnectionError, requests.TooManyRedirects, requests.Timeout), e:
            print e

    def get_content_concurrent(self, json_metadata):
        """
        Uses multiple threads to scrape the content of posts concurrently
        """
        threads = len(json_metadata)/4  # Number of threads to create

        # Create a list of jobs and then iterate through
        # the number of threads appending each thread to
        # the job list
        jobs = []
        for i in range(0, threads):
            thread = threading.Thread(target=self.get_content, args=(json_metadata[i],))
            jobs.append(thread)
            thread.start()
        for j in jobs:
            j.join()


def main():

    # Scrape using 4 processes and multi-threading

    client = MongoClient()
    scraper = MultiScraper(client, "hacker_news", "hacker_posts", )
    t = Timer(lambda: scraper.get_metadata("data/dates"))
    print "Took %s seconds to scrape data using 4 cores." % t.timeit(number=1)
    conn.close()


if __name__ == '__main__':
    main()
