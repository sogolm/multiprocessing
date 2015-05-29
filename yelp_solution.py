from timeit import Timer
from yelp_helpers import search
from yelp_helpers import scrape_business_info
import multiprocessing
import threading
import yelp_helpers


def get_business_info_threads(ids):
    threads = len(ids)  # Number of threads to create

    # Create a list of jobs and then iterate through
    # the number of threads appending each thread to
    # the job list
    jobs = []
    for i in range(0, threads):
        thread = threading.Thread(target=scrape_business_info, args=(ids[i],))
        jobs.append(thread)
        thread.start()
    for j in jobs:
        j.join()


def scrape_parallel(pool_num):
    yelp_helpers.coll.remove({})
    pool = multiprocessing.Pool(pool_num)

    with open('data/cities') as f:
        cities = f.read().splitlines()
        output = pool.map(search, cities)
        pool.close()
        pool.join()
        business_ids = [x['id'] for y in output for x in y['businesses']]
        get_business_info_threads(business_ids)


def scrape_sequential():
    yelp_helpers.coll.remove({})
    with open('data/cities') as f:
        cities = f.read().splitlines()
        for city in cities:
            response = search(city)
            business_ids = [x['id'] for x in response['businesses']]
            for business_id in business_ids:
                scrape_business_info(business_id)


if __name__ == '__main__':
    t = Timer(lambda: scrape_sequential())
    print "Completed sequential in %s seconds." % t.timeit(1)

    t2 = Timer(lambda: scrape_parallel(4))
    print "Completed parallel in %s seconds." % t2.timeit(1)