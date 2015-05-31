from timeit import Timer
from yelp_helpers import request
from pymongo import MongoClient
import multiprocessing
import threading
import os
from collections import Counter

POOL_SIZE = 4
API_HOST = "api.yelp.com"
SEARCH_PATH = '/v2/search'
BUSINESS_PATH = '/v2/business/'

DB_NAME = "yelp"
COLLECTION_NAME = "business"

client = MongoClient()
db = client[DB_NAME]
coll = db[COLLECTION_NAME]
counter = Counter()


def search_parallel(city):
    """
    Makes a request to Yelp's search API given the city name.
    :param city:
    :return: JSON meta data for top 20 businesses.
    """
    params = {'location': city, 'limit': 20}
    json_response = request(API_HOST, SEARCH_PATH, url_params=params)
    businesses = json_response['businesses']
    business_ids = [x['id'] for x in businesses]
    get_business_info_threads(business_ids)


def get_business_info_threads(ids):
    threads = len(ids)  # Number of threads to create

    jobs = []
    for i in range(0, threads):
        thread = threading.Thread(target=scrape_business_info, args=(ids[i],))
        jobs.append(thread)
        thread.start()
    for j in jobs:
        j.join()


def scrape_parallel(pool_size):
    coll.remove({})
    pool = multiprocessing.Pool(pool_size)

    with open('data/cities') as f:
        cities = f.read().splitlines()
        pool.map(search_parallel, cities)
        pool.close()
        pool.join()


def scrape_business_info(business_id):
    """
    Makes a request to Yelp's business API and retrieves the business data in JSON format.
    Dumps the JSON response into mongodb.
    :param business_id:
    """
    business_path = BUSINESS_PATH + business_id
    response = request(API_HOST, business_path)
    coll.insert(response)


def search(city):
    """
    Makes a request to Yelp's search API given the city name.
    :param city:
    :return: JSON meta data for top 20 businesses.
    """
    params = {'location': city, 'limit': 20}
    json_response = request(API_HOST, SEARCH_PATH, url_params=params)
    return json_response


def scrape_sequential():
    """
    Scrapes the business's meta data for a list of cities
    and for each business scrapes the content.
    """
    coll.remove({})  # Remove previous entries from collection in Mongodb.
    with open('data/cities') as f:
        cities = f.read().splitlines()
        for city in cities:
            response = search(city)
            business_ids = [x['id'] for x in response['businesses']]
            for business_id in business_ids:
                scrape_business_info(business_id)


if __name__ == '__main__':
    # t = Timer(lambda: scrape_sequential())
    # print "Completed sequential in %s seconds." % t.timeit(1)

    t2 = Timer(lambda: scrape_parallel(POOL_SIZE))
    print "Completed parallel in %s seconds." % t2.timeit(1)