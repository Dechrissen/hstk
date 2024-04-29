from Functions import *
from Analysis import *
from Tokenizer import *
from Trigrams import *
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
# total: stores True when used
parser.add_argument("-t", "--total", action="store_true", help="display the total number of headline snaps in the databse")
# random : takes one optional argument of type int, where its default is 1 (const=1)
parser.add_argument("-r", "--random", metavar=("NUMBER"), nargs="?", const=1, type=int, help="display a random headline snap from the database")
# convert : stores True when used
parser.add_argument("-c", "--convert", action="store_true", help="convert headline snap image files in /data/src/raw then add them to the database")
# dump : stores True when used
parser.add_argument("-d", "--dump", action="store_true", help="dump all headline snaps in the database to a text file at /data/dump.txt")
# DEBUG: zaddtestfile : stores True when used
parser.add_argument("-z", "--zaddtestfile", action="store_true")
# search : takes one mandatory argument of type str
parser.add_argument("-s", "--search", metavar=("PHRASE"), type=str, help="search the headline snap database for snaps containing PHRASE")

# parser.add_argument("-v", "--visualizer")

# SUBPARSER: Define options
# add subparser arguments
tokenizer_parser = subparsers.add_parser("tokenizer", help="tokenizer-related commands")
tokenizer_parser.add_argument("-u", "--update_tokens", action="store_true", help="update the token database with new counts")

# parse arguments from command line input and save to `args`
args = parser.parse_args()

# run `args` through functions to check each argument
getTotalSnaps(args.total)
getRandomSnap(args.random)
searchSnaps(args.search)
if args.convert:
    convertDirectory(r"./data/src/raw")
    addToSnapDatabase(db_file=r"./data/db/hs.db", text_file=r"./data/src/text/ocr_output.txt")

if args.dump:
    dumpAll()

# debug
if args.zaddtestfile:
    addToSnapDatabase(db_file=r"./data/db/hs.db", text_file=r"./data/src/text/test_file.txt")

# check to see if subparsers were invoked
if args.subparser == "tokenizer":
    # check if individual subparser options were used
    if args.update_tokens:
        updateTokens()

# tokenizer and clean function test
#print(tokenizeSnap("this,    Is a Test::: super-cool man-eating test. test! snap"))

#print(addToTokenDatabase(r"./data/db/tokens.db", "vehicle", 1))


# debug: print Namespace to see arg values, then exit
print('\n' + 'DEBUG: ' + str(args) + '\n')

print("trigram tests ...")
#dumpCorpus()
test_model = trainTrigramModel(corpus_path)
print(generateSentence(test_model))

print("ending...")
raise SystemExit(1)