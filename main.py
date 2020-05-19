from infix_to_postfix import match_regex
from InvalidRegexException import InvalidRegexException

import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Need 2 arguments.')
        exit(1)

    try:
        if match_regex(sys.argv[1], sys.argv[2]):
            print('Matches.')
        else:
            print('Does not match.')
    except InvalidRegexException:
        print('Invalid regular expression.')
    except:
        print('Unknown error.')
