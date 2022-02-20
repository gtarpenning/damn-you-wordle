""" Local CLI Interface, imports from main worlde file """
import numpy as np
import logging

from deploy.backend.wordle_assistant import *

def main():
    """ Command Line Interface for Local Interaction """
    answers, allowed = load_word_lists()
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
            guess_dict = make_guess_dict(allowed_left, answers_left)
            find_entropies(guess_dict, answers_left, best_flag=best_flag, local=True)
    
    
if __name__ == '__main__':
    main()
