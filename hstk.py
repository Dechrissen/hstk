from Functions import *
from Analysis import *
import os
from argparse import ArgumentParser
from pathlib import Path # not using this yet

# Argument parsing

# set program name and description
parser = ArgumentParser(
    prog="hstk",
    description="Toolkit for working with a database of Headline Snaps",
)

# define options
parser.add_argument("-t", "--total", action="store_true", help="display the total number of headline snaps in the databse")
parser.add_argument("-r", "--random", action="store_true", help="display a random headline snap from the database")
parser.add_argument("-d", "--dummy", action="store_true", help="dummy option")
# parser.add_argument("-v", "--visualizer")
# parser.add_argument("-c", "--create-database")

# parse arguments from command line input and save to args
args = parser.parse_args()

# run args through functions that correspond to arguments
getTotalSnaps(total=args.total)

# REMOVE
if args.dummy:
    print("dummy option has been used")
print("ending...")
raise SystemExit(1)



initialize()

# test for converting a directory of snaps (images) to strings
#convertDirectory('./data/src/raw')

# test for creating sqlite db
db_file = r"./data/db/hs.db"
text_file = r"./data/src/text/test_file.txt"
createDatabase(db_file)
addToDatabase(db_file, text_file)
