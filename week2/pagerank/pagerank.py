import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob_dict = {}
    n_pages = len(corpus)
    n_links = len(corpus[page])
    
    if n_links != 0:
        for apage in corpus:
            prob_dict[apage] = (1 - DAMPING) / n_pages
        for link in corpus[page]:
            prob_dict[link] = prob_dict[link] + (DAMPING / n_links)
    elif n_links == 0:
        for apage in corpus:
            prob_dict[apage] = 1 / n_pages
    
    for k,v in prob_dict.items():
        prob_dict[k] = round(v, 5)
             
    
    return(prob_dict)


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample_count = {}
    
    for key in corpus.keys():
        sample_count[key] = 0
    
    
    start_page = random.choice(list(corpus.keys()))
    next_dict = transition_model(corpus, start_page, damping_factor)
    
    for N in range(n - 1):  
        next_page = random.choices(list(next_dict.keys()), weights=list(next_dict.values()), k=1)[0]
        sample_count[next_page] += 1
        next_dict = transition_model(corpus, next_page, damping_factor)
    
    
    sample_prob = {}
    for k,v in sample_count.items():
        sample_prob[k] = v/n

    return sample_prob

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    pr_last = {}
    pr_next = {}
    diff = {}
    
    for key in corpus.keys():
        pr_last[key] = 1/len(corpus)
        pr_next[key] = 0
        diff[key] = 1
        
    while max(diff.values()) >= 0.001:
        for query_page in pr_next:
            for k,v in corpus.items():
                for link in v:
                # Look for incoming links and calculate PR based on previous
                # PR and number of total links on incoming link site
                    if link == query_page:
                        pr_next[query_page] += (pr_last[k] / len(corpus[k]))
            pr_next[query_page] = pr_next[query_page] * damping_factor
            # Random chance to land on page
            pr_next[query_page] += ((1 - damping_factor) / len(corpus))
        # Calculate change in PR
        for page in diff:
            diff[page] = abs(pr_next[page] - pr_last[page])    
        
        #Replace last with next and start over
        pr_last = pr_next.copy()
        for k in pr_next:
            pr_next[k] = 0
    
    return(pr_last)
if __name__ == "__main__":
    main()
