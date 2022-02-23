""" Local CLI Interface, imports from main worlde file """
import numpy as np
import logging

from deploy.backend.wordle_assistant import *


def local_load_word_lists():
    """ Load in word lists for possible 5 letter words """
    allowed = []
    with open("./data/wordle-allowed-guesses.txt", "r") as f:
        allowed = f.read().split('\n')

    logging.info(f"Loaded [{len(allowed)}] possible words to guess")

    answers = []
    with open("./data/wordle-answers-alphabetical.txt", "r") as f:
            answers = f.read().split('\n')

    logging.info(f"Loaded [{len(answers)}] possible wordles")
    return answers, allowed


def main():
    """ Command Line Interface for Local Interaction """
    answers, allowed = local_load_word_lists()
    answers_left = answers.copy()
    allowed_left = allowed.copy()
    while True:
        raw_input = input("Input guess, wordle template. (Example: crane, OO--X)\n\n > ")
        if "," not in raw_input:
            print("Misformatted input")
            continue

        guess, template = raw_input.split(",")
        answers_left = narrow_down(guess.strip(), template.strip(), answers_left)
        allowed_left = narrow_down(guess.strip(), template.strip(), allowed_left)
        
        print(f"Nice! You narrowed down possible words to just [{len(answers_left)}] left.")
        answer = input("Would you like a breakdown of possible next choices? (y/n) \n"
                        "Pass -b for just a breakdown of the best choices \n\n > ")
    
        best_flag = '-b' in answer
        if 'y' in answer:
            guess_dict = make_candidate_lookup(allowed_left, answers_left)
            print(guess_dict)
            find_entropies(answers_left, allowed_left, guess_dict, best_flag=best_flag, local=True)
    
    
if __name__ == '__main__':
    main()
