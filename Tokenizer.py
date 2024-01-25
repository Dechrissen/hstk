from Functions import *

def updateTokens():
    print("updateTokens function has been invoked")

def tokenizeSnap(snap):
    '''Extracts unique tokens from a Headline Snap and assigns counts to each.

    args
        snap : a Headline Snap to be tokenized

    returns
        tokenized_snap : a dictionary of token:count (string:int) pairs
    '''

    # split snap (string) into list of tokens
    snap_as_list = snap.split()
    for index in range(len(snap_as_list)):
        snap_as_list[index] = cleanText(snap_as_list[index])

    tokenized_snap = {}

    # add each token and its count to tokenized_snap
    for token in snap_as_list:
        tokenized_snap[token] = tokenized_snap.get(token, 0) + 1

    return tokenized_snap
        

    