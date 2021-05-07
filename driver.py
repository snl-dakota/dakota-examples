#!/usr/bin/env python

def hello_fn():
    """
    Just a placeholder for work to follow ...
    """

    print("What to do next ...")
    return 42



if __name__ == "__main__":

    meaning_of_life = hello_fn()
    assert(42 == meaning_of_life),'expected to find the meaning of life.'
