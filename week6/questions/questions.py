import nltk
import sys
import string
import os
import math

FILE_MATCHES = 5
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
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    
    return_dict = {}
    for page in os.listdir(os.path.join(os.getcwd(), "corpus")):
        with open(os.path.join(os.getcwd(), "corpus", page), "r", encoding="utf8") as file:
            data = file.read().replace('\n','')
        return_dict[page] = data

    return return_dict

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    
    document = nltk.word_tokenize(document)
    
    for i, token in enumerate(document):
        document[i] = token.lower()
        document[i] = token.translate(str.maketrans('','', string.punctuation))
        if token in nltk.corpus.stopwords.words("english"):
            document.remove(token)
    
    return document        

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    
    return_dict = {}
    all_words = set()
    
    for words in documents.values():
        for word in words:
            all_words.add(word)
    
    for word in all_words:
        counter = 0
        for document in documents:
            if word in documents[document]:
                counter += 1
        return_dict[word] = math.log(len(documents) / counter)       

    return return_dict

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    
    return_list = []
    
    for document in files:
        sum_tf_idfs = 0
        for word in query:
            tf = 0
            tf_idf = 0
            if word in files[document]:
                tf = files[document].count(word)
            tf_idf = tf - idfs[word]
            sum_tf_idfs += tf_idf
        return_list.append((document, sum_tf_idfs))
                      
    return_list.sort(key=lambda tup: tup[1], reverse=True)
    return_list = [item[0] for item in return_list]
    return return_list[0:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    
    return_list = []
    
    for sentence in sentences:
        sum_idfs = 0
        for word in query:
            idf = 0
            if word in sentences[sentence]:
                idf = idfs[word]
            sum_idfs += idf     
        return_list.append((sentence, sum_idfs))
    
    return_list.sort(key=lambda tup: tup[1], reverse=True)
    return_list = [item[0] for item in return_list]
    return return_list[0:n]
          

if __name__ == "__main__":
    main()
