import argparse

from sub import *


banner = '''
Subliminally: Create Subliminals Easily
\n\n'''


parser = argparse.ArgumentParser(description=banner)

# required arguments
parser.add_argument('-t', '--title', required=True, help='title for your subliminal') # title argument
parser.add_argument('-a', '--affs', required=True, help='text file of the affirmations for your subliminal')  # affirmations argument
parser.add_argument('-b', '--bg', required=True, help='audio file for your subliminal') # background argument
parser.add_argument('-i', '--img', required=False, help='image file for your subliminal') # image argument

args = parser.parse_args()


print(banner)


sub_creator(args.title, args.affs, args.bg)
