from Functions import *
from Analysis import *
from Tokenizer import *
from argparse import ArgumentParser

# this only runs if "initialized":false in cache.json
# so if the project has been initialized once, it won't run again
initialize()


# ARGUMENT PARSING
# ----------------

# set program name and description
parser = ArgumentParser(
    prog="hstk",
    description="Toolkit for working with a database of Headline Snaps",
)

# add subparsers for specific functions, example: tokenizer-related ones
subparsers = parser.add_subparsers(
    # set dest="subparser" so that we can access it in the Namespace later
    title="subcommands", dest="subparser", help="subcommands for database-interfacing"
)

# MAIN PARSER: Define options
# total: stores True when used
parser.add_argument("-t", "--total", action="store_true", help="display the total number of headline snaps in the databse")
# random : takes one optional argument of type int, where its default is 1 (const=1)
parser.add_argument("-r", "--random", metavar=("NUMBER"), nargs="?", const=1, type=int, help="display a random headline snap from the database")
# convert : stores True when used
parser.add_argument("-c", "--convert", action="store_true", help="convert headline snap image files in /data/src/raw then add them to the database")
# debug: zaddtestfile : stores True when used
parser.add_argument("-z", "--zaddtestfile", action="store_true")

# parser.add_argument("-v", "--visualizer")

# add subparser arguments
tokenizer_parser = subparsers.add_parser("tokenizer", help="tokenizer-related commands")
tokenizer_parser.add_argument("-u", "--update_tokens", action="store_true", help="update the token database with new counts")

# parse arguments from command line input and save to `args`
args = parser.parse_args()

# run `args` through functions to check each argument
getTotalSnaps(args.total)
getRandomSnap(args.random)
if args.convert:
    convertDirectory(r"./data/src/raw")
    addToDatabase(db_file=r"./data/db/hs.db", text_file=r"./data/src/text/output.txt")

# debug
if args.zaddtestfile:
    addToDatabase(db_file=r"./data/db/hs.db", text_file=r"./data/src/text/test_file.txt")

# check to see if subparsers were invoked
if args.subparser == "tokenizer":
    # check if individual subparser options were used
    if args.update_tokens:
        updateTokens()

print(tokenizeSnap("this,    Is a Test::: test. test! snap"))

# debug: print Namespace to see arg values, then exit
print(args) 
print("ending...")
raise SystemExit(1)