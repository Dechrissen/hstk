from nltk import trigrams
from collections import defaultdict
import random
from pathlib import Path
from time import sleep

# must run dumpCorpus before this file exists
corpus_path = r"./data/corpus.txt"

def trainTrigramModel(corpus_path):
    '''Trains a trigram language model.
    
    args
        corpus_path : the path to the training corpus

    returns
        model : a dictionary containing the trigram model
    '''
    # TODO: try making this 0?
    # Smoothing of 0.01 to handle unattested words in test data 
    model = defaultdict(lambda: defaultdict(lambda: 0.01))

    # TODO make this use headline snap data somehow, not iterate through txt files in a directory

    # train model on full corpus of headline snaps
    print("Training a trigram model on the database of Headline Snaps ...")
    with open(corpus_path, 'r', encoding='utf-8') as f:
        sents = f.readlines()
        for sentence in sents:
            sentence = sentence.split()
            for w1, w2, w3 in trigrams(sentence, pad_right=True, pad_left=True):
                model[(w1, w2)][w3] += 1

    # transform the counts into probabilities
    for w1_w2 in model:
        total_count = float(sum(model[w1_w2].values()))
        for w3 in model[w1_w2]:
            model[w1_w2][w3] /= total_count
    sleep(1)
    print("Done.\n")
    return model

def generateSentence(trigram_model, corpus_path):
    '''Generates a sentence according to a trigram model.
    
    args
        trigram_model : the trigram model to use in sentence generation

    returns
        generated : the generated sentence
    '''
    text = [None, None]
    generated = ''
    sentence_finished = False
    # instantiate counter to keep track of times tried to generate a novel sentence
    fail_counter = 0
    max_tries = 10

    sleep(1)
    print("Generating a new Headline Snap ...\n")
    sleep(1)

    while not sentence_finished:
        r = random.random()
        accumulator = .0
        for word in trigram_model[tuple(text[-2:])].keys():
            accumulator += trigram_model[tuple(text[-2:])][word]
            if accumulator >= r:
                text.append(word)
                break
        # preemptively create the generated sentence (string) here, because we need to check it against the corpus anyway
        generated = ' '.join([t for t in text if t])
        # check if the sentence is complete AND not present in the corpus verbatim
        if (text[-2:] == [None, None]) and not checkAgainstCorpus(generated,corpus_path):
            sentence_finished = True
        # else (meaning it is in the corpus), check only if it's finished
        elif text[-2:] == [None, None]:
            # increment the number of novel sentence generation tries
            fail_counter += 1           
            # DEBUG
            #print("Times failed: ", fail_counter)
            if fail_counter == max_tries:
                # if we reach max tries, give up and return the sentence anyway
                sentence_finished = True
                continue
            # set the sentence back to the starting value (empty with padding) before trying again
            text = [None, None]

    disclaimer = "\n" if (fail_counter < max_tries) else " (maximum reached; sentence not novel)\n"
    print("Non-novel generations before novelty achieved:", str(fail_counter) + disclaimer)
    #generated = ' '.join([t for t in text if t])
    return generated

def checkAgainstCorpus(sentence,corpus_path):
    '''Checks if a given sentence is present in a given corpus file.
    
    args
        sentence : the sentence to check
        corpus_path : the path to the corpus file to be compared to

    returns
        bool
    '''
    with open(corpus_path, 'r', encoding='utf-8') as corpus_file:
        # need to use .read().splitlines() here as opposed to readlines()
        # so we do not get '\n' at the end of every list item
        # this allows the sentence being checked against the list to match if necessary
        sents = corpus_file.read().splitlines()
        if sentence in sents:
            return True
        else:
            return False
