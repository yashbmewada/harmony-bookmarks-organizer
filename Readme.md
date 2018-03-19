# Harmony - A Simple Bookmarks Organizer

Everyone faces a problem once in a while, when trying to switch browsers that each browser has multiple bookmarks. Some of them are even duplicates.

Harmony is a simple bookmarks organizer built with python 3.6 which provides you with a consolidated list of bookmarks that are reorganized based on following rules:

- Links with same domain name occur in same list.

- Links with shorter length occur before the larger one.

- Links with `https` occur before the links with `http`.

- Links that are redirected to other url would appear after the link they are redirected to ( provided the destination url also exists in the bookmark list). for example, `https://www.google.com/news` is redirected to `https://news.google.com/news` (this would occur first in the list as it is destination.)

## Input

List of bookmarks from all your browsers. Currently you can provide three lists namely Safari, Chrome and Firefox.

```
`safari = [
      'https://mail.google.com/mail/u/0/#inbox',
    'https://www.concur.com/',
    'https://www.sap.com/index.html',
    'https://www.google.com/news/',
      'https://www.google.com/images/']

chrome = [
      'https://mail.google.com/',
    'https://github.com/',
    'https://stackoverflow.com/',
    'https://www.sap.com',
      'https://images.google.com/',
      'https://www.google.com/imghp']

firefox = [
      'https://mail.google.com/',
    'https://github.com/',
    'http://www.sap.com/',
    'https://news.google.com/news/']
```

## Output

```
Working on organising your bookmarks...
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████| 15/15 [00:04<00:00,  2.60it/s]


Just a few final touches....
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 8/8 [00:02<00:00,  4.63it/s]


Your bookmarks are now organised!!!!

[['https://mail.google.com/', 'https://mail.google.com/mail/u/0/#inbox'], 
 ['https://www.concur.com/'], 
 ['https://www.sap.com/index.html', 'https://www.sap.com', 'http://www.sap.com/'], 
 ['https://news.google.com/news/', 'https://www.google.com/news/'], 
 ['https://www.google.com/imghp', 'https://www.google.com/images/'], 
 ['https://github.com/'], 
 ['https://stackoverflow.com/'], 
 ['https://images.google.com/']
```



## How to run

1. Clone the repository or download zip .

   ```
   git clone https://github.com/yashbmewada/harmony-bookmarks-organizer.git
   ```

   

2. Before proceeding, you must have python 3.x installed on your system. run the follwing command from terminal or command prompt to check if you have python installed.

   ```
   python
   ```

   OR

   ```
   python3
   ```

   ( NOTE: we will require python3.x version.)

   

3. If already installed, use the following command to run the script.

   ```
   python app.py # this must point to the python3 binary in your system 
   ```

   OR

   ```
   python3 app.py
   ```

4. Congratulations!! you are ready to organize your bookmarks.

## BruteForce Approach

To solve this problem the most simple way can be to compare each item with another and based on the strings, as well as redirect url just putting in simple lists, which would be much costlier and take a lot of time to run.

## Approach To Current Solution

1. The main function has list provided in the input. (It can also be read from file but for simplicity of demonstration I have kept as three different lists. any of the list can be empty in that case the current solution would not be affected.) 

2. A  universal list called `all_links_list` which appends all the urls together helps get together and process all the bookmarks.

3. Then, a dictionary which has `domain-name` as *key* with `[ similar urls by domain]` as *value* for each key. This gives us the organized list of links accessible through the key. ( `domain-name` is extracted by `extract_domain` method which takes in a link and checks for redirection through `check_redirect` and `get_redirected_url` methods to ensure that the final redirected destination should be used as the `domain-name` )  For example, [https://google.com/news] is always redirected to [https://news.google.com/news] so it makes sense to put them together as one key called `news.google.com`. 

   The dictionary for above input  looks like as follows :

   ```
   {'mail.google.com': ['https://mail.google.com/mail/u/0/#inbox', 'https://mail.google.com/'], 
    'www.concur.com': ['https://www.concur.com/'], 
    'www.sap.com': ['https://www.sap.com/index.html', 'https://www.sap.com', 'http://www.sap.com/'], 
    'news.google.com': ['https://www.google.com/news/', 'https://news.google.com/news/'], 
    'www.google.com': ['https://www.google.com/images/', 'https://www.google.com/imghp'], 
    'github.com': ['https://github.com/'], 'stackoverflow.com': ['https://stackoverflow.com/'], 
    'images.google.com': ['https://images.google.com/']}
   ```

4. Now just iterating through each key, the lists are sorted using custom comparators as follows:

   - Length (shorter length is preferred)

   - presence of ssl ( https links first) `check_ssl` method.

   - presence of redirection( destination to which a link is redirected preferred) `check_redirect` method acts as comparator.

5. A list of organized bookmarks is printed.

## Possible Optimizations and Bottlenecks

- The biggest bottleneck in this case comes at *checking for redirection* (Network Bound ). I have tried with a concurrent approach using threading but it also produced similar results due to inconsistency of the library to make Asynchronous request. 

- To solve this, I have tried to drive the user attention by enabling progressbars in the simple solution. it provides a better user experience than just waiting idly at screen.

- An implementation of `asyncio` can be added which can allow async network requests. But to keep the solution as barebone as possible (and time constraints) , I have not added that.

- Another method can be to create a `ThreadPool` where the size of the pool can be `min( number of cores *2 , length of url list)` as the machine can allow us to easily spawn around `number of cores *2 ` threads very safely. Also, spawning that many threads can be considered feasible as the cost would not be as big as overhead of a netweork request.

- Thus, the solution has the best performance if implemented with Asynchronous requests.

In case you wish to contribute, generate an issue and create a pull request.
