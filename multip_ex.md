In this section, we are going to explore the [multiprocessing](https://docs.python.org/2/library/multiprocessing.html) module. The function primes_sequential in primes.py finds prime numbers between 100000000 and 101000000 by iterating through the list of numbers one by one and check their primality. 
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

1. Implement primes_parallel using a pool size of 4 (or the number of cores on your machine) and observe the time imporovement in execution.
2. Run parallel version of the script again and use the following script in shell to see all the processes running that are attached to the execution of primes.py

```shell
ps aux | grep primes.py
```
3. Verify the number of processes running. 
4. Each process has a unique id attached to it called the **PID**. You can explore which process is running at any given point in your code by using the getpid() in the os module. 



iterable to map?, how to find out the number of cores on machine?