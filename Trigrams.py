from nltk import trigrams
from collections import defaultdict
import random
from pathlib import Path
import os

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

    return model

def generateSentence(trigram_model):
    '''Generates a sentence according to a trigram model.
    
    args
        trigram_model : the trigram model to use in sentence generation

    returns
        generated : the generated sentence
    '''
    text = [None, None]
    sentence_finished = False

    while not sentence_finished:
        r = random.random()
        accumulator = .0
        for word in trigram_model[tuple(text[-2:])].keys():
            accumulator += trigram_model[tuple(text[-2:])][word]
            if accumulator >= r:
                text.append(word)
                break
        if text[-2:] == [None, None]:
            sentence_finished = True

    generated = ' '.join([t for t in text if t])
    return generated

