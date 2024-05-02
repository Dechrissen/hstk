import json

# This script takes an a9t9 output file 'a9t9.txt' and converts it into a cleaned
# file 'a9t9_cleaned.txt' (e.g. no Snapchat-specific text, no stray newlines, etc.),
# with one headline snap per line.

# define filters to remove from the string
try:
    with open("../config.json", "r") as jsonFile:
        config = json.load(jsonFile)
except FileNotFoundError:
    print("ERROR: Config file not found; please run hstk.py first to perform initial setup.")
    raise SystemExit(1)

filters = config["filters"]

# DEBUG
#print(filters)
#print(type(filters))
#raise SystemExit(1)
# ---

print('Cleaning a9t9 output file ...')

# read in a9t9 output as a full string
with open("a9t9.txt", "r") as f:
    raw_content = f.read()

x = raw_content

# replace instances of 'Send a chat', etc. with empty string
for filter in filters:
    x = x.replace(filter + ' \n', '')

# split into a list at newline characters
lines = x.split('\n')

# start a counter to get list indeces
c = 0
for line in lines:
    # replace the a9t9 separator with a pipe
    if '===' in line:
        lines[c] = '|'
    c += 1

# join this back into a string (at this point there are no newline characters)
x = "".join(lines)
x = x.split(' |')

# write each line to a file 'a9t9_cleaned.txt'
# one headline snap per line
with open('../data/src/text/a9t9_cleaned.txt', 'w', encoding='utf-8') as f:
    for line in x:
        f.write(line + '\n')

print('Done.')
print('Cleaned output file is available at /data/src/text/a9t9_cleaned.txt')
