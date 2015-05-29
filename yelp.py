from timeit import Timer
from yelp_helpers import search
from yelp_helpers import scrape_business_info
import yelp_helpers

POOL_SIZE = 4


def scrape_parallel():
    pass


def scrape_sequential():
    """
    Scrapes the business's meta data for a list of cities
    and for each business scrapes the content.
    """
    yelp_helpers.coll.remove({}) # Remove previous entries from collection in Mongodb.
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

    t2 = Timer(lambda: scrape_parallel(POOL_SIZE))
    print "Completed parallel in %s seconds." % t2.timeit(1)