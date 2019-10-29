"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    new_list = []
    for x in range(len(paragraphs)):
        if select(paragraphs[x]):
            new_list.append(paragraphs[x])
    if k > len(new_list) - 1:
        return ''
    else:
        return new_list[k]
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def check(words):
        words = remove_punctuation(lower(words))
        words = split(words)
        for x in words:
            if x in topic:
                return True
        return False
    return check
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    correct = 0.0
    denominator = len(typed_words)
    if len(typed_words) > len(reference_words):
        typed_words = typed_words[:len(reference_words)]
    elif len(typed_words) < len(reference_words):
        for x in range(len(reference_words) - len(typed_words)):
            typed_words.append('x')
    for x in range(len(reference_words)):
        if reference_words[x] == typed_words[x]:
            correct += 1
    if denominator == 0:
        return 0.0
    return correct / denominator * 100

    "*** YOUR CODE HERE ***"
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    characters = 0
    for character in typed:
        characters += 1
    words = characters / 5
    factor = 1
    if elapsed != 60:
        factor = 60 / elapsed
        elapsed = 60
    words = factor * words
    return words
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    good_word = ""
    lowest_difference = limit + 1

    for word in valid_words:
        if word == user_word:
            return word
        difference = diff_function(user_word, word, limit)
        if difference < lowest_difference:
            good_word = word
            lowest_difference = difference
    if lowest_difference > limit:
        return user_word
    else:
        return good_word

    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    # assert False, 'Remove this line'
    count = 0
    def diff(start, goal, limit, count):
        if len(start) == 0:
            return count
        if count > limit:
            return limit + 1
        if len(start) > len(goal):
            return diff(start[:len(start)-1], goal, limit, count + 1)
        if len(start) < len(goal):
            return diff(start, goal[:len(goal)-1], limit, count + 1)
        if start[-1] != goal[-1]:
            return diff(start[:len(start)-1], goal[:len(goal)-1], limit, count + 1)
        else:
            return diff(start[:len(start)-1], goal[:len(goal)-1], limit, count)
    return diff(start, goal, limit, count)
    # END PROBLEM 6

def edit_diff(start, goal, limit, count=0):
    """A diff function that computes the edit distance from START to GOAL."""
    # assert False, 'Remove this line'

    if goal == "" and start == "": # Fill in the condition
        # BEGIN
        "*** YOUR CODE HERE ***"
        return 0
        # END
    if goal == "" and start != "":
        return len(start)

    if goal != "" and start == "":
        return len(goal)

    if goal[0] == start[0]: # Feel free to remove or add additional cases
        # BEGIN
        "*** YOUR CODE HERE ***"
        return edit_diff(start[1:], goal[1:], limit, count)
        # END

    if count > limit:
        return limit + 1

    else:
        add_diff = 1 + edit_diff(start, goal[1:], limit, count + 1)  # Fill in these lines
        remove_diff = 1 + edit_diff(start[1:], goal, limit, count + 1)
        substitute_diff = 1 + edit_diff(start[1:], goal[1:], limit, count + 1)
        # BEGIN
        "*** YOUR CODE HERE ***"
        return min(add_diff, remove_diff, substitute_diff)
        # END


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    if len(prompt) > len(typed):
        for x in range(len(prompt) - len(typed)):
            typed += ['hello']
    typed_correctly = 0
    for x in range(len(prompt)):
        if typed[x] == prompt[x]:
            typed_correctly += 1
        else:
            break
    progress = {"id": id, "progress": typed_correctly / len(prompt)}
    send(progress)
    return progress["progress"]
    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    all_times, player_list = [], []
    for x in range(1, len(word_times[0])):
        player_time = []
        for player in word_times:
            player_time.append(elapsed_time(player[x]) - elapsed_time(player[x-1]))
        all_times.append(player_time)

    for time in range(len(word_times)):
        temp_player = []
        for player in range(len(all_times)): # ask bill to explain
            if all_times[player][time] <= min(all_times[player]) + margin: # ask bill to explain
                temp_player += [word(word_times[time][player + 1])] # ask bill to explain
        player_list.append(temp_player)
    return player_list
    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
