import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj NP VP | NP VP Conj VP
NP -> N | Det N | Det AP N | NP P NP | P Det N 
VP -> V | V NP | V Adv | Adv V NP | V NP Adv | V P NP
AP -> Adj | Adj Adj | Adj Adj Adj
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    print("\nInput:",sentence)
    sentence = nltk.word_tokenize(sentence)
    
    for i, token in enumerate(sentence):
        sentence[i] = token.lower()
        if not token.isalpha():
            non_alpha = 0
            for letter in token:
                if not letter.isalpha():
                    non_alpha += 1
                if len(token) == non_alpha:
                    sentence.remove(token)        
                
    return sentence
def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    
    ptree = nltk.tree.ParentedTree(0,[])
    ptree = ptree.convert(tree)
    return_list = []
    
    for chunk in ptree.subtrees():
        if chunk.label() == "N":
            print(chunk.parent())
                    
                
    return return_list

if __name__ == "__main__":
    main()
