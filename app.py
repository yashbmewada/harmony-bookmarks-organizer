#################################################################
# Harmony - A simple bookmarks organizer                        #
# Author: Yash Bhaveshkumar Mewada                              # 
# Email : ybmewada@gmail.com                                    #
#################################################################

import requests
from tqdm import tqdm


#extracts domain from a given url of the form www.google.com / news.google.com 
def extract_domain(link):
    """ Function that extracts and returns the domain name from the string url passed.
        for e.g. http://www.google.com/helloworld/index would return www.google.com (if URL has redirection,
        the redirected url is returned.)
    """
    if check_redirect(link) == 1:
        link = get_redirect_url(link)
    link_wo_http = link.split('//')[-1]
    link_domain = link_wo_http.split('/')[0]
    return link_domain


#checks the links redirects or not (also serves as a comparator)
def check_redirect(link):
    """ Function that checks if a url is redirected to other link.
        Also works as a comparator for sorting.
        returns 1 if a url is redirected to other.
        returns 0 if a url is not redirected.
    """
    response = requests.head(link)
    redirect_code_list = [302,301,307,303,308]
    if response.status_code in redirect_code_list:
        return 1
    else:
        return 0


#if link redirects, get the link where it redirects
def get_redirect_url(link):
    """
        Function to retreive which url the link is redirected to.
        e.g. http://www.google.com/news returns http://news.google.com/news/
    """
    response = requests.get(link)
    if response.history:
        if response.url != link:
            return response.url
        else:
            return link


#checks Https present or not
def check_ssl(link):
    """ Comparator that helps in sorting based on whether the link has HTTPS or not.
        Links which return 0 has https, and hence would appear first if a list is sorted
        using this function as a key.
    """
    if link.startswith('https'):
        return 0
    else:
        return 1




if __name__ == "__main__":
    safari = ['https://mail.google.com/mail/u/0/#inbox',
    'https://www.concur.com/',
    'https://www.sap.com/index.html',
    'https://www.google.com/news/','https://www.google.com/images/']
    chrome = ['https://mail.google.com/',
    'https://github.com/',
    'https://stackoverflow.com/',
    'https://www.sap.com','https://images.google.com/','https://www.google.com/imghp']
    firefox = ['https://mail.google.com/',
    'https://github.com/',
    'http://www.sap.com/',
    'https://news.google.com/news/']
    
    all_links_list = safari + chrome + firefox #generating a single list of all links
    result_list = []
    progress_counter = 0 #used for progressbar
    print("Working on organising your bookmarks...")
    pbar = tqdm(total=len(all_links_list))#progressbar for better UX.
    url_dict = dict()
    #generating the dictionary with structure {'domain-name' : [list of urls with that domain]}.
    for link in all_links_list:
        key = extract_domain(link)
        if key in url_dict.keys():
            url_list = url_dict[key]
            if link not in url_list:
                url_list.append(link)
        else:
            url_dict[key] = [link]
        pbar.update(progress_counter+1)
    pbar.close()
    print("\n")
    print("Just a few final touches....")
    pbar = tqdm(total=len(url_dict))
    progress_counter = 0
    #sorting the lists of similar urls from dictionary according to rules in problem.
    for key in list(url_dict.keys()):
        same_url_list = url_dict[key]
        same_url_list = sorted(same_url_list ,key=lambda x:len(x))
        same_url_list = sorted(same_url_list ,key=lambda x:check_ssl(x))
        same_url_list = sorted(same_url_list ,key=lambda x:check_redirect(x))
        result_list.append(same_url_list )
        pbar.update(progress_counter+1)
    pbar.close()
    print("\n")
    print("Your bookmarks are now organised!!!! \n")        
    print(result_list)

