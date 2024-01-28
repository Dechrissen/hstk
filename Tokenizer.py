from Functions import *

def updateTokens():
    # this function should iterate over every (new?) snap in the snap db
    # using tokenizeSnap for each
    # and adding each token to the token db with addToTokenDatabase()
    # to only check NEW snaps (maybe), we could use a value in a json to save the last headline snap row that has been checked,
    # then start from there when this function is run again
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
        

    