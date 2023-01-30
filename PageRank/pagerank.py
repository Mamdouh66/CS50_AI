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
    # ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    # print(f"PageRank Results from Sampling (n = {SAMPLES})")
    # for page in sorted(ranks):
    #     print(f"  {page}: {ranks[page]:.4f}")
    # ranks = iterate_pagerank(corpus, DAMPING)
    # print(f"PageRank Results from Iteration")
    # for page in sorted(ranks):
    #     print(f"  {page}: {ranks[page]:.4f}")
    ranks = transition_model(corpus, "recursion.html", DAMPING)
    # print(f"PageRank Results from Iteration")
    # for page in sorted(ranks):
    #     print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
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

    # a dict. that has all the keys from corpus, N num. of key
    transModel = dict().fromkeys(corpus)
    N = len(dict.fromkeys(corpus))

    if len(corpus[page]) == 0:  # if it has no links, just act that as it has one to all pages
        for key in transModel:
            transModel[key] = 1/N
        return transModel

    # Probabilty of piciking a page in random
    damping_probabilty = round((1-damping_factor) / N, 4)

    for key in transModel:
        transModel[key] += damping_probabilty
        # if page had a link for it, then the surfer should go to them with equal prob.
        if key in corpus[page]:
            transModel[key] += (damping_factor/N)

    return transModel


def sample_pagerank(corpus, damping_factor, n):
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
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
