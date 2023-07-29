import argparse

from sub_maker import *
from video_maker import *


banner = '''
Subliminally: Create Subliminals Easily
\n\n'''


parser = argparse.ArgumentParser(description=banner)

# title argument
parser.add_argument('-t', '--title', required=True, help='title for your subliminal')
# affs argument
parser.add_argument('-a', '--affs', required=True, help='text file of the affirmations for your subliminal')
# bg argument
parser.add_argument('-b', '--bg', required=True, help='audio file for your subliminal')
# img argument
parser.add_argument('-i', '--img', required=True, help='image file for your subliminal')

args = parser.parse_args()


print(banner)


sub_creator(args.title, args.affs, args.bg)
video_creator(args.title, args.img)
