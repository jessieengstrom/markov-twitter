"""Generate Markov text from text files."""

from random import choice

from sys import argv

import twitter

import os


def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    with open(file_path) as our_file:

        return our_file.read()


def make_chains(text_string, size):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.
    """

    chains = {}

    words = text_string.split()
    words.append(None)

    for i in range(len(words) - size):

        n_gram = tuple([word for word in words[i:i + size]])

        if n_gram not in chains:
            chains[n_gram] = []

        chains[n_gram].append(words[i + size])

    return chains


def make_text(chains):
    """Return text from chains."""
    start_keys = [key for key in chains.keys() if key[0][0].isupper()]
    current_key = choice(start_keys)
    end_punctuation = (".", "?", "!")
    words = []

    while True:
        if current_key[-1] is None:
            words.extend(current_key[:-1])
            return check_length(words)

        else:
            for i in range(len(current_key)):
                if current_key[i][-1] in end_punctuation:
                    words.extend(current_key[:i + 1])
                    return check_length(words)

        words.append(current_key[0])
        next_value = choice(chains[current_key])
        current_key = current_key[1:] + (next_value,)


def check_length(words):
    """Checks potential tweets for appropriate length"""
    tweet_text = " ".join(words)
    if len(tweet_text) > 140 or len(tweet_text) <= 60:
        return make_text(chains)

    else:
        return tweet(tweet_text)


def tweet(tweet_text):
    """Create a tweet and send it to the Internet."""

    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    status = api.PostUpdate(tweet_text)

    play_again = raw_input("Enter to tweet again or q to quit > ")

    if play_again == "q":
        quit()
    else:
        make_text(chains)

    return status.text


input_path = argv[1]
n_gram_size = int(argv[2])

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text, n_gram_size)

# Produce random text
tweet_text = make_text(chains)
print tweet_text

# tweet_it = tweet(tweet_text)

# print tweet_it
