from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
from timeit import Timer
from pymongo import errors


API_HOST = 'http://hckrnews.com/data/'


class Scraper():
    """
    Uses the hackernews api to scrape articles' meta data and content sequentially and insert it into MongoDB
    """

    def __init__(self, client, mongodb_name, collection_name):
        self.client = client
        self.db = self.client[mongodb_name]
        if collection_name in self.db.collection_names():
            self.db[collection_name].drop()
        self.coll = self.db[collection_name]

    def get_posts_metadata(self, dates_path):
        """
        Scrapes posts meta-data along with each link's content
        """
        with open(dates_path) as f:
            dates = f.read().splitlines()
            for date in dates:
                url = API_HOST + date + ".js"
                try:
                    response = requests.get(url, timeout=3)
                    if response.status_code == 200:
                        posts = response.json()
                        for post_meta in posts:
                            self.get_post_content(post_meta)
                except (requests.ConnectionError, requests.TooManyRedirects, requests.Timeout), e:
                    print e

    def get_post_content(self, post_metadata):
        """
        Scrapes the content of a post given a single entry in json and loads the json into mongodb
        """
        url = post_metadata[u'link']
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content)
                content_text = soup.get_text()
                post_metadata['content'] = content_text
                try:
                    self.coll.insert(post_metadata)
                except errors.DuplicateKeyError:
                    print "Duplicates"
        except (requests.ConnectionError, requests.TooManyRedirects, requests.Timeout), e:
            print e


def main():
    client = MongoClient()
    scraper = Scraper(client, "hacker_news", "hacker_posts")
    t = Timer(lambda: scraper.get_posts_metadata("data/dates"))
    print "Took %s seconds to scrape using one process" % t.timeit(number=1)
    client.close()


if __name__ == '__main__':
    main()