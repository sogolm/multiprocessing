In this section, we're going to use multiprocessing and threading to scrape Yelp. 

1. Take a look at [Yelp's API documentation](https://www.yelp.com/developers/documentation) and get your authentication set up by [generating new token/secret](https://www.yelp.com/developers/manage_api_keys) if you haven't already. 
We're going to use the [search](https://www.yelp.com/developers/documentation/v2/search_api) (for searching based on city names) and [business](https://www.yelp.com/developers/documentation/v2/business) (to look up business info by ids that we retrieved from search). 

The function `scrape_sequential` in `yelp.py` uses the search API to scrape the top 20 business ids for 4 cities listed in [data/cities](FIX LINK). Then it uses the business API to scrape info for each business id. Since this is done sequentially, it's very slow. 

`yelp_helpers.py` includes all the helper functions you need to make requests to search and business APIs. Note that `scrape_business_info` dumps the JSON response (including the business info for one business) into Mongodb. The only change you need to make to this file is putting your authentication info on top (which is not generally a good practice).

2. Run yelp.py and note how long it takes to complete.

3. Our goal is to use a separate process for each city and hit the search API. We also want to use multithreading within each process for each business id to hit the business API. Use the multiprocessing pool and threading libraries from the previous sections to implemenet scrape_parallel and any additional helper functions that you need. Note that you don't have to change the helper functions in `yelp_helpers.py` but feel free to do so if you need to. 

[FIX THIS] (https://github.com/sogolm/multiprocessing/img/multiprocessing.jpg)





