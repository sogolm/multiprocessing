import multiprocessing
import requests
import sys
import threading
from timeit import Timer


def request_item(item_id):
    try:
        print 'Starting thread %s\n' % threading.currentThread().getName()
        r = requests.get("http://hn.algolia.com/api/v1/items/%s" % item_id)
        print 'Exiting thread %s\n' % threading.currentThread().getName()
        return r.json()
    except requests.RequestException:
        return None


def request_sequential():
    sys.stdout.write("Requesting sequentially...\n")

    for item_id in range(1, 20):
        request_item(item_id)

    sys.stdout.write("done.\n")

def request_concurrent():
    sys.stdout.write("Requesting in parallel...\n")
    pass

if __name__ == '__main__':
    t = Timer(lambda: request_sequential())
    print "Completed sequential in %s seconds." % t.timeit(1)
    print "--------------------------------------"

    t = Timer(lambda: request_concurrent())
    print "Completed using threads in %s seconds." % t.timeit(1)
