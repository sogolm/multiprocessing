In this section, we're going use the [Threading](https://docs.python.org/2/library/threading.html) module on Python. Threading module allows a program to run multiple operations *concurrently* in the same process space. The use of threads speed up the execution of programs that are I/O bound, where the execution of a task involves some waiting -- e.g. programs that access data from a network address or hard disk -- One way of speeding up such code is to generate a thread for each item that needs to be accessed. 

Consider a Python code that is scraping many URLS. Each URL will have a download time. In a single-threaded implementation, the Python interpreter spends most of its time waiting for the results of each URL to come back. By using a separate thread for each URL, the code can download the data sources in parallel without waiting on previous downloads to finish. Let's see this in practice.

The code in [request_example.py](FIX THIS LINK) uses the [Hacker News Unofficial API](https://hn.algolia.com/api) to access the meta data for Hacker News posts by id. So for example sending a GET request to [http://hn.algolia.com/api/v1/items/:id](http://hn.algolia.com/api/v1/items/13) returns a JSON object containing the meta data for post with id 13.

The function, request_sequential, sends a request for posts with ids between 1 and 20. This function is using only one thread of execution (the main thread) and is spends most of the time waiting for the responses. 

Our goal is to implement request_concurrent to use threads for downloading the contents of each URL.

The simplest way to use a thread is to instantiate a Thread object with a target function along with the arguments to the target function as a tuple. Then we  call start() to let it begin working.

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
A call to a thread x join() will make the calling thread (in this case the main thread of our program) wait until the the thread x is terminated. So we want to wait until all threads in our jobs list finish executing before exiting.

1. Fill out the request_concurrent function to create and execute threads for each request. Run the script and compare the execution times for the sequential requests vs. concurrent requests. 

2. We want to be able to determine which thread is running at any given time. Each Thread instance has a name with a default value that can be overwritten upon creating the thread. Naming threads is useful in more complicated server processes where each thread is responsible for handling different operations. Pass in a name to the Thread constructor and uncomment the print functions. Run the script and see the order of execution of threads. 

Happy concurrency!












