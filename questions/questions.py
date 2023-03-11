import nltk
import sys
import string
import math
import os

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):

    files = {}
    for File in os.listdir(directory):
        path = os.path.join(directory, File)
        with open(path, mode="r") as f:
            files[File] = f.read()
    return files


def tokenize(document):

    tokens = []

    for word in nltk.word_tokenize(document.lower()):
        if word in string.punctuation or word in nltk.corpus.stopwords.words("english"):
            continue
        else:
            tokens.append(word)
    return tokens


def compute_idfs(documents):

    idfs = {}
    word_counter = {}

    for document in documents:
        for word in set(documents[document]):
            if word not in word_counter:
                word_counter[word] = 1
            else:
                word_counter[word] += 1

    for word in word_counter:
        idfs_value = math.log(len(documents)/word_counter[word])
        idfs[word] = idfs_value

    return idfs


def top_files(query, files, idfs, n):

    scores = {File: 0 for File in files}

    for word in query:
        for File in files:
            if word in files[File] and idfs:
                tf = files[File].count(word)
                tfidf = tf * idfs[word]
                scores[File] += tfidf

    sorted_scores = [key for key, value in sorted(
        scores.items(), key=lambda File: File[1], reverse=True)]
    return sorted_scores[:n]


def top_sentences(query, sentences, idfs, n):

    best_sentences = {}

    for sentence in sentences:
        sentence_score = 0
        for word in query:
            if word in sentences[sentence]:
                sentence_score += idfs[word]
        if sentence_score != 0:
            total = 0
            for word in query:
                total += sentences[sentence].count(word)

            qtd_value = total / len(sentences[sentence])
            best_sentences[sentence] = (sentence_score, qtd_value)

    sorted_by_score = [k for k, v in sorted(
        best_sentences.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)]

    return sorted_by_score[:n]


if __name__ == "__main__":
    main()
