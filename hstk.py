from Functions import *
from Analysis import *
from Tokenizer import *
from Trigrams import *
from Visualizer import *
from argparse import ArgumentParser

# this only runs if "initialized":false in cache.json
# so if the project has been initialized once, it won't run again
initialize()


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
    title="subcommands", dest="subparser", help="toolkit subcommands"
)

# MAIN PARSER: Define options
# add : stores True when used
parser.add_argument("-a", "--add", action="store_true", help="adds the current contents of /data/src/text/ocr_output.txt to the database")
# total: stores True when used
parser.add_argument("-t", "--total", action="store_true", help="display the total number of headline snaps in the databse")
# random : takes one optional argument of type int, where its default is 1 (const=1)
parser.add_argument("-r", "--random", metavar=("INT"), nargs="?", const=1, type=int, help="display a random headline snap from the database")
# convert : stores True when used
parser.add_argument("-c", "--convert", action="store_true", help="convert headline snap image files in /data/src/raw then add them to the database")
# dump : stores True when used
parser.add_argument("-x", "--export", action="store_true", help="dump all headline snaps from the database to a text file at /data/dump.txt")
# search : takes one mandatory argument of type str
parser.add_argument("-s", "--search", metavar=("STR"), type=str, help="search the headline snap database for snaps containing STR (in quotes)")
# delete : stores True when used
parser.add_argument("-d", "--delete", action="store_true", help="delete all data from the headline snap and token databases")


# SUBPARSER: Define options

# add subparser arguments
tokenizer_parser = subparsers.add_parser("tokenizer", help="tokenizer commands")
tokenizer_parser.add_argument("-u", "--update_tokens", action="store_true", help="update the token database with new counts")

trigram_parser = subparsers.add_parser("trigrams", help="trigram model commands")
trigram_parser.add_argument("-g", "--generate", action="store_true", help="train a trigram model on the database and generate a new headline")

visualizer_parser = subparsers.add_parser("visualizer", help="visualization commands")
visualizer_parser.add_argument("-w", "--word_cloud", action="store_true", help="generate and display a word cloud of the most common words in the database")

# parse arguments from command line input and save to `args`
args = parser.parse_args()

# run `args` through functions to check each argument
getTotalSnaps(args.total)
getRandomSnap(args.random)
searchSnaps(args.search)
if args.convert:
    convertDirectory(r"./data/src/raw")
    addToSnapDatabase(db_file=r"./data/db/hs.db", src_text_dir=r"./data/src/text")

if args.export:
    dumpAll()

if args.add:
    addToSnapDatabase(db_file=r"./data/db/hs.db", src_text_dir=r"./data/src/text")

if args.delete:
    deleteDatabases(hsdb_path=r"./data/db/hs.db",token_db_path=r"./data/db/tokens.db")

# SUBPARSER CHECKS

# check to see if tokenizer subparser was invoked
if args.subparser == "tokenizer":
    # check if individual subparser options were used
    if args.update_tokens:
        updateTokens()

# check to see if trigrams subparser was invoked
if args.subparser == "trigrams":
    # check if individual subparser options were used
    if args.generate:
        #dumpCorpus() TODO uncomment this
        trigram_model = trainTrigramModel(corpus_path)
        print(generateSentence(trigram_model))

if args.subparser == "visualizer":
    # check if individual subparser options were used
    if args.word_cloud:
        #dumpCorpus() TODO uncomment this
        generateWordCloud()

# DEBUG tokenizer and clean function test
#print(tokenizeSnap("this,    Is a Test::: super-cool man-eating test. test! snap"))
#print(addToTokenDatabase(r"./data/db/tokens.db", "vehicle", 1))


sleep(2)
# DEBUG print Namespace to see arg values, then exit
print('\n' + 'DEBUG: ' + str(args) + '\n')



print("Exiting ...")
raise SystemExit(1)