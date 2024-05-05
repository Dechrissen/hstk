from Functions import *
from Analysis import *
from Tokenizer import *
from Trigrams import *
from Visualizer import *
from argparse import ArgumentParser

# define some relevant paths
hs_db_path = r"./data/db/hs.db"
token_db_path = r"./data/db/tokens.db"
src_images_path = r"./data/src/raw"
src_text_path=r"./data/src/text"
corpus_path = r"./data/corpus.txt" # this won't exist until dumpCorpus() function is run

# this only runs if "initialized":false in cache.json
# so if the project has been initialized once, it won't run again
initialize(hs_db_path, token_db_path)

# ARGUMENT PARSING
# ----------------

# set program name and description
parser = ArgumentParser(
    prog="hstk",
    description="hstk - headline snap toolkit",
)

# add subparsers for specific functions, example: tokenizer-related ones
subparsers = parser.add_subparsers(
    # set dest="subparser" so that we can access it in the Namespace later
    title="subcommands", dest="subparser", help=""
)

# MAIN PARSER: Define options
# add : stores True when used
parser.add_argument("-a", "--add", action="store_true", help="add the current contents of the files in /data/src/text to the database")
# total: stores True when used
parser.add_argument("-t", "--total", action="store_true", help="display the total number of headline snaps in the databse")
# random : takes one optional argument of type int, where its default is 1 (const=1)
parser.add_argument("-r", "--random", metavar=("NUM"), nargs="?", const=1, type=int, help="display a random headline snap from the database")
# convert : stores True when used
parser.add_argument("-c", "--convert", action="store_true", help="convert headline snap image files in /data/src/raw then add them to the database")
# dump : stores True when used
parser.add_argument("-x", "--export", action="store_true", help="dump all headline snaps from the database to a text file at /data/dump.txt")
# search : takes one mandatory argument of type str
parser.add_argument("-s", "--search", metavar=("STR"), type=str, help="query the headline snap database for entries containing STR (in quotes)")
# delete : stores True when used
parser.add_argument("-d", "--delete", action="store_true", help="delete all data from the headline snap and token databases")


# SUBPARSER: Define options

# add subparser arguments
tokenizer_parser = subparsers.add_parser("tokenizer", help="headline snap tokenizer commands")
tokenizer_parser.add_argument("-u", "--update_tokens", action="store_true", help="update the token database with new counts")
tokenizer_parser.add_argument("-q", "--query_tokens", metavar=("TKN"), type=str, help="print number of times some individual token TKN (in quotes) appears in the database")

trigram_parser = subparsers.add_parser("trigrams", help="trigram language model commands")
trigram_parser.add_argument("-g", "--generate", action="store_true", help="train a trigram model on the database and generate a new headline")

visualizer_parser = subparsers.add_parser("visualizer", help="data visualization commands")
visualizer_parser.add_argument("-w", "--word_cloud", action="store_true", help="generate and display a word cloud of the most common words in the database")

# parse arguments from command line input and save to `args`
args = parser.parse_args()

# run `args` through functions to check each argument
getTotalSnaps(hs_db_path, args.total)
getRandomSnap(hs_db_path, args.random)
searchSnaps(hs_db_path, args.search)
if args.convert:
    convertDirectory(src_images_path)
    addToSnapDatabase(hs_db_path, src_text_path)

if args.export:
    dumpAll(hs_db_path)

if args.add:
    addToSnapDatabase(hs_db_path, src_text_path)

if args.delete:
    deleteDatabases(hs_db_path, token_db_path)

# SUBPARSER CHECKS

# check to see if tokenizer subparser was invoked
if args.subparser == "tokenizer":
    # check if individual subparser options were used
    if args.update_tokens:
        dumpCorpus(hs_db_path) # so the updateTokens() function has an up-to-date corpus to work with
        updateTokens(token_db_path)
    if args.query_tokens:
        token = cleanText(args.query_tokens)
        print("Querying token database for token \"" + token + "\" ...")
        sleep(1)
        count = getTokenCount(token_db_path, token)
        if count != 0:
            print("Count:", count)
        else:
            print("Token not present in database.")


# check to see if trigrams subparser was invoked
if args.subparser == "trigrams":
    # check if individual subparser options were used
    if args.generate:
        dumpCorpus(hs_db_path) # so the trainTrigramModel() function has an up-to-date corpus to work with
        trigram_model = trainTrigramModel(corpus_path)
        print('\t' + generateSentence(trigram_model, corpus_path))

if args.subparser == "visualizer":
    # check if individual subparser options were used
    if args.word_cloud:
        dumpCorpus(hs_db_path) # so the generateWordCloud() function has an up-to-date corpus to work with
        generateWordCloud()

# DEBUG tokenizer test
#print(tokenizeSnap("this,    Is a Test::: super-cool man-eating test. test! snap"))
#addToTokenDatabase(r"./data/db/tokens.db", "parkour", 1)

# DEBUG print Namespace to see arg values, then exit
#print('\n' + 'DEBUG: ' + str(args) + '\n')

sleep(1)
print("\nExiting ...")
raise SystemExit(1)