# Versatile collection of tools to enable quick & easy development in Python 3.12+

import zdev.base as base
# fixme: import all modules already as pkg head?!?

def main(verbose=False):
    if (verbose):
         print("Welcome to the 'zdev' package!")
         print("Initialising Python...")
    base.init_session(base._BASE, base._ENVIRONMENT, verbose)
    if (verbose): print("...done - have phun! ;)")

main(True) # call 'init_session' with internal defaults if only 'import zdev'!

    