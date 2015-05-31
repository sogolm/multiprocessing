# Part 1 -- multiprocessing 

In this section, we are going to explore the [multiprocessing](https://docs.python.org/2/library/multiprocessing.html) module. The function `primes_sequential` in primes.py finds prime numbers between 100000000 and 101000000 by iterating through the list of numbers one by one and check their primality. 
Run the script and note  how long it takes to execute.
This is an example of a problem that can be divided into sub-problems -- tasks -- that can be computed in parallel on multiple cores. The multiprocessing library in Python spawns multiple operating system processes for each parallel task and will feed each process to a separate processor core. 
We will be using python's multiprocessing's Pool class to create a pool of worker processes. The map method in Pool class has basically the same functionality as the built-in map(), except that individual tasks run in parallel. 

```python
import multiprocessing

def some_function(lst):
	...

pool = multiprocessing.Pool(processes=number_of_processes)
outputs = pool.map(func=some_function, iterable)
pool.start()
pool.join()
```

The map function chops the iterable into a number of chunks which it submits to the process pool as separate tasks and is input to the function specified. 
The call to join() will make the main calling process wait until all processes are done with their tasks.
You can also use the function apply_async in most cases. 

1. Implement `primes_parallel` using a pool size of 4 (or the number of cores on your machine) and observe the time imporovement in execution.
2. Run parallel version of the script again and use the following script in shell to see all the processes running that are attached to the execution of `primes.py`

```shell
ps aux | grep primes.py
```
3. Verify the number of processes running. 
4. Each process has a unique id attached to it called the **PID**. You can explore which process is running at any given point in your code by using the getpid() in the os module. 

# Part 2 -- threading

In this section, we're going use the [Threading](https://docs.python.org/2/library/threading.html) module on Python. Threading module allows a program to run multiple operations *concurrently* in the same process space. The use of threads speed up the execution of programs that are I/O bound, where the execution of a task involves some waiting -- e.g. programs that access data from a network address or hard disk -- One way of speeding up such code is to generate a thread for each item that needs to be accessed. 

Consider a Python code that is scraping many URLS. Each URL will have a download time. In a single-threaded implementation, the Python interpreter spends most of its time waiting for the results of each URL to come back. By using a separate thread for each URL, the code can download the data sources in parallel without waiting on previous downloads to finish. Let's see this in practice.

The code in `request_example.py` uses the [Hacker News Unofficial API](https://hn.algolia.com/api) to access the meta data for Hacker News posts by id. So for example sending a GET request to [http://hn.algolia.com/api/v1/items/13](http://hn.algolia.com/api/v1/items/13) returns a JSON object containing the meta data for post with id 13.

The function, `request_sequential`, sends a request for posts with ids between 1 and 20. This function is using only one thread of execution (the main thread) and spends most of its time waiting for the responses. 

Our goal is to implement `request_concurrent` to use threads for downloading the contents of each URL.

The simplest way to use a thread is to instantiate a Thread object with a target function along with the arguments to the target function as a tuple. Then we call start() to let it begin working.

```python
def target_function(arg1, arg2):
	...

t = threading.Thread(target=target_function, args=(arg1, arg2))
t.start()
```

In our case we want to use one thread for each URL so we need to create these threads and start them in a for loop.

```python
jobs = []
for i in range(num_threads):
	t = threading.Thread(target=target_function, args=(arg1, arg2))
	jobs.append(t)
	t.start()
for t in jobs:
	t.join()
```
A call to a thread join() will make the calling thread (in this case the main thread of our program) wait until the thread is terminated. So we want to wait until all threads in our jobs list finish executing before exiting.

1. Fill out the `request_concurrent` function to create and execute threads for each request. Run the script and compare the execution times for the sequential requests vs. concurrent requests. 

2. We want to be able to determine which thread is running at any given time. Each Thread instance has a name with a default value that can be overwritten upon creating the thread. Naming threads is useful in more complicated server processes where each thread is responsible for handling different operations. Pass in a name to the Thread constructor and uncomment the print functions. Run the script and see the order of execution of threads. Happy concurrency!

# Part 3

In this section, we're going to use multiprocessing and threading to scrape Yelp. 

1. Take a look at [Yelp's API documentation](https://www.yelp.com/developers/documentation) and get your authentication set up by [generating new token/secret](https://www.yelp.com/developers/manage_api_keys) if you haven't already. 
We're going to use the [search](https://www.yelp.com/developers/documentation/v2/search_api) (for searching based on city names) and [business](https://www.yelp.com/developers/documentation/v2/business) (to look up business info by ids that we retrieved from search). 

The function `scrape_sequential` in `yelp.py` uses the search API to scrape the top 20 business ids for 4 cities listed in [data/cities](FIX LINK). Then it uses the business API to scrape info for each business id. Since this is done sequentially, it's very slow. 

`yelp_helpers.py` includes all the helper functions you need to make requests to search and business APIs. Note that `scrape_business_info` dumps the JSON response (including the business info for one business) into Mongodb. The only change you need to make to this file is putting your authentication info on top (which is not generally a good practice).

2. Run `yelp.py` and note how long it takes to complete.

3. Our goal is to use a separate process for each city and hit the search API. We also want to use multithreading within each process for each business id to hit the business API. Use the multiprocessing pool and threading libraries from the previous sections to implemenet scrape_parallel and any additional helper functions that you need. Note that you don't have to change the helper functions in `yelp_helpers.py` but feel free to do so if you need to. 

![Image of multiprocessing -- fix this] (https://github.com/zipfian/high_performance_python/blob/master/img/multiprocessing.jpg)