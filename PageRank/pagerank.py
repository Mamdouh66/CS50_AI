import os
import random
import re
import sys
import pandas as pd
import numpy as np
DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    # ! TBD
    # ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    # print(f"PageRank Results from Sampling (n = {SAMPLES})")
    # for page in sorted(ranks):
    #     print(f"  {page}: {ranks[page]:.4f}")
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


# def transition_model(corpus, page, damping_factor):
#     """
#     Return a probability distribution over which page to visit next,
#     given a current page.

#     With probability `damping_factor`, choose a link at random
#     linked to by `page`. With probability `1 - damping_factor`, choose
#     a link at random chosen from all pages in the corpus.
#     """
#     raise NotImplementedError


# def sample_pagerank(corpus, damping_factor, n):
#     """
#     Return PageRank values for each page by sampling `n` pages
#     according to transition model, starting with a page at random.

#     Return a dictionary where keys are page names, and values are
#     their estimated PageRank value (a value between 0 and 1). All
#     PageRank values should sum to 1.
#     """
#     raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # define const. N: num of links, rank: a dict that keeps track of the page rank
    # pageRank : here we save the values for the formula, iterations: will determine how many times we loop
    N = len(dict.fromkeys(corpus))
    rank = dict.fromkeys(corpus)
    pageRank = 0.0
    iterations = 0

    # assign initial probabilty 1/N
    for key in rank:
        rank[key] = 1 / N

    # Recursive loop
    while True:
        # re-initilize iterations to zero
        iterations = 0
        for key in corpus:  # for each page KEY in the corpus
            pageRank = 0.0
            for value in corpus:  # for each other page in the corpus
                if key in corpus[value]:  # if it has a link to the KEY page
                    # get the summation of these pages pageRank
                    pageRank += (rank[value]/len(corpus[value]))
                elif not corpus[value]:  # if no page links to page KEY
                    # see its rank in the dict
                    page_rank_no_links = rank[value]
                    page_probability = page_rank_no_links / N  # act as it has links to all pages
                    pageRank += page_probability  # add its probabilty to the pageRank

            pageRank = ((1-damping_factor) / N) + (damping_factor *
                                                   pageRank)  # calculate the complete formula
            # if the diffrence is tiny, add an iteration
            if abs(rank[key] - pageRank) < 0.0001:
                iterations += 1
            rank[key] = pageRank  # update the page rank

        if iterations == N:  # if every page has a tiny diffrence, just break
            break

    # ! debugging
    # sum = 0
    # for key in rank:
    #     print(key, " = ", round(rank[key], 4))
    #     sum += rank[key]
    # print(round(sum, 4))

    return rank


if __name__ == "__main__":
    main()
