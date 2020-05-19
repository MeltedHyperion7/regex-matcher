# Regex Matcher
Script that uses Thompson's algorithm to match regular expressions.
The regular expressions supported are very basic, only supporting the *, +, and | operations. This does not make them any less powerful, however.
## Instructions
Run in a shell
`python3 main.py <regex> <string to match>`
## Thompson's Algorithm
Thompson's algorithm is asymptotically faster than the regular expression matching algorithms used by languages like Python, PHP and Perl because it does not rely on recursive backtracking. These languages support extensions to actual regular expressions, such as backr references, which make them more powerful. However implementing these extensions means that their algorithms run in exponential time in the length of the string on some inputs. Thompson's algorithm does not have this drawback. A hybrid implementation could also be achieved that turns to backtracking only when it has to deal with back references.
## Inspiration
https://swtch.com/~rsc/regexp/regexp1.html
https://dl.acm.org/doi/10.1145/363347.363387