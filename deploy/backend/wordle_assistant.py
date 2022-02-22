from collections import Counter, defaultdict
import numpy as np
import logging
import json


def load_word_lists():
    """ Load in word lists for possible 5 letter words """
    allowed = []
    with open("../../data/wordle-allowed-guesses.txt", "r") as f:
        allowed = f.read().split('\n')

    logging.info(f"Loaded [{len(allowed)}] possible words to guess")

    answers = []
    with open("../../data/wordle-answers-alphabetical.txt", "r") as f:
        answers = f.read().split('\n')

    logging.info(f"Loaded [{len(answers)}] possible wordles")
    return answers, allowed


def make_candidate_lookup_table(answers, allowed, template_lookup):
    """ 
    Build JSON for candidate lookup table of shape: 
    table {
        candidate1 {
            template {
                [word1, word2, ... ]
            }
            ...
        }
    }
    """
    candidate_lookup = {}
    for candidate in answers + allowed:
        candidate_lookup[candidate] = defaultdict(list)
        for (word, template) in template_lookup[candidate].items():
            candidate_lookup[candidate][template] += [word]
    
    with open('../../data/candidate_lookup.json', 'w') as f:
        json.dump(candidate_lookup, f)

    return candidate_lookup


def make_template_lookup_table(answers, allowed):
    """ 
    Build template lookup table of shape: 
    table {
        candidate1 {
            candidate 2 {
                template
            }
        }
    }
    """
    template_lookup = {}
    for word1 in allowed + answers:
        template_lookup[word1] = {}
        for word2 in answers:
            template_lookup[word1][word2] = make_template(word1, word2)

    with open('../../data/template_lookup.json', 'w') as f:
        json.dump(template_lookup, f)

    return template_lookup


def load_lookup_tables(answers, allowed):
    """ Load pre-computed lookup tables """
    import os

    logging.info(os.listdir())

    t_lookup, cand_lookup = None, None

    if 'template_lookup.json' not in os.listdir('../../data'):
        t_lookup = make_template_lookup_table(answers, allowed)

    if 'candidate_lookup.json' not in os.listdir('../../data'):
        cand_lookup = make_candidate_lookup_table(answers, allowed, t_lookup)

    if not cand_lookup:
        with open("../../data/candidate_lookup.json", "r") as f:
            cand_lookup = json.load(f)

    if not t_lookup:
        with open("../../data/template_lookup.json", "r") as f:
            t_lookup = json.load(f)
    
    return cand_lookup, t_lookup


def check_cand(guess, template, candidate, cand_lookup=None):
    """ 
    True if guess and hit/miss template is compatible 
    for a given possible answer candidate 
    Significant performance gain when using the lookup table
    """
    if cand_lookup and candidate in cand_lookup[guess]:
        # Speedup only works for some cached values
        return candidate in cand_lookup[guess][template]
    
    for l1, l2, t in zip(guess, candidate, template):
        if l1 in candidate and t == '-':
            return False
        if l1 not in candidate and t == 'O':
            return False
        if l1 == l2 and t != 'X':
            return False
        if l1 != l2 and t == 'X':
            return False
    return True


def narrow_down(guess, template, words_left, c_lookup=None):
    """ 
    Accepts a wordle guess, and the number of words left;
    returns list of remaining possible words 
    """
    return [c for c in words_left if check_cand(guess, template, c, c_lookup)]


def make_template(pred, gold, t_lookup=None):
    """ Helper func to create worlde-like template 
        input two words and get a "XO---" 
            "X": hit
            "O": in word
            "-": not in word """
    if t_lookup:
        return t_lookup[pred][gold]
    
    gold_counter = Counter(gold)

    template = ""
    for (l1, l2) in enumerate(zip(pred, gold)):
        if l1 == l2:
            template += "X"
            gold_counter[l1] -= 1
        elif l1 in gold_counter and gold_counter[l1] > 0:  # Buggy template creation fix
            template += "O"
            gold_counter[l1] -= 1
        else:
            template += "-"
    return template


def make_guess_dict(allowed_left, answers_left, c_lookup=None, t_lookup=None):
    """ Return a dictionary of shape:
        guess word {
            possible_template_1 {
                [word1_given_template1, word2_given_template1, ...]
            }
            possible_template_2 {}
                    .
                    .
        }
            """
    g_dict = {}
    all_left = allowed_left + answers_left
    all_left.sort()  # Looks neater
    for guess in all_left: # a possible word that is allowed
        g_dict[guess] = {}
        for answer in answers_left:  # a potential answer
            template = make_template(guess, answer, t_lookup)
            g_dict[guess][template] = narrow_down(guess, template, answers_left)
    
    return g_dict


def calc_entropy(words):
    """ 
    Helper function to calculate some metric of uncertainty 
    proportional to the probability of getting a template and
    the number of guesses in the future required to resolve 
    words resulting from said template
    """
    return len(words) * np.log2(len(words))


def find_entropies(answers_left, allowed_left, c_lookup, best_flag=False, local=False):
    """ 
    Calculates the entropy of all possible guesses remaining, 
    only printing out the best guesses if passing best_flag=True
    """
    entropy_bin = []
    for guess in answers_left + allowed_left:
        entropy = sum([calc_entropy(c_lookup[guess][t]) for t in c_lookup[guess]])
        entropy_bin += [(guess, entropy)]

    entropy_bin.sort(key=lambda x: x[1], reverse=True)
    best = []
    for (guess, entropy_val) in entropy_bin: 
        # Special case when possible last word, only guess real answers
        if entropy_val == 0 and guess not in answers_left:
            continue
        elif entropy_val == entropy_bin[-1][1]:
            best += [(guess, entropy_val)]

    """ Printing for local environment """
    if local:
        print("Best guess(es): ")
        for (guess, entropy_val) in best:
            print(f"* {guess} [{entropy_val}]")
            for template in c_lookup[guess]:
                print(f".... {template}:  {', '.join(c_lookup[guess][template])}")

    return best


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

        # Local dev input
        # raw_input = 'crane, -O--X'
        # answer = 'y -b'

        guess, template = raw_input.split(",")
        answers_left = narrow_down(guess.strip(), template.strip(), answers_left)
        allowed_left = narrow_down(guess.strip(), template.strip(), allowed_left)
        
        print(f"Nice! You narrowed down possible words to just [{len(answers_left)}] left.")
        answer = input("Would you like a breakdown of possible next choices? (y/n) \n"
                        "Pass -b for just a breakdown of the best choices \n\n > ")
    
        best_flag = '-b' in answer
        if 'y' in answer:
            guess_dict = make_guess_dict(allowed_left, answers_left)
            find_entropies(guess_dict, answers_left, best_flag=best_flag)
    
    
if __name__ == '__main__':
    main()
