import numpy as np


def load_word_lists():
    """ Load in word lists for possible 5 letter words """
    allowed = []
    with open("./wordle-allowed-guesses.txt", "r") as f:
        allowed = f.read().split('\n')

    print(f"Loaded [{len(allowed)}] possible words to guess")

    answers = []
    with open("./wordle-answers-alphabetical.txt", "r") as f:
            answers = f.read().split('\n')

    print(f"Loaded [{len(answers)}] possible wordles")
    return answers, allowed


def check_cand(guess, template, candidate):
    """ True if guess and hit/miss template is compatible 
        for a given possible answer candidate """
    for l1, l2, t in zip(guess, candidate, template):
        if l1 == l2 and t != 'X':
            return False
        if l1 != l2 and t == 'X':
            return False
        if l1 not in candidate and t == 'O':
            return False
        if l1 in candidate and t == '-':
            return False
    return True


def narrow_down(guess, template, words_left):
    """ Accepts a wordle guess, and the number of words left;
        defaults to all possible words left (for 1st turn) 
        and returns list of remaining possible words """
    return [cand for cand in words_left if check_cand(guess, template, cand)]


def make_template(pred, gold):
    """ Helper func to create worlde-like template 
        input two words and get a "XO---" 
            "X": hit
            "O": in word
            "-": not in word """
    template = ""
    for l1, l2 in zip(pred, gold):
        if l1 == l2:
            template += "X"
        elif l1 in gold:
            template += "O"
        else:
            template += "-"
    return template


def make_guess_dict(allowed_left, answers_left):
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
            template = make_template(guess, answer)
            g_dict[guess][template] = narrow_down(guess, template, answers_left)
    
    return g_dict


def find_entropies(g_dict, best_flag=False):
    """ Calculates the entropy of all possible guesses remaining, 
        only printing out the best guesses if passing best_flag=True """
    entropy_bin = []
    for guess in g_dict:
        print_str = ""
        entropy = 0
        for template in g_dict[guess]:
            print_str += f"\n.... {template}:  {', '.join(g_dict[guess][template])}"
            entropy += np.log2(len(g_dict[guess][template]))
        print_str = f"\n{guess}, Entropy score: [{entropy}] {print_str}\n"
        entropy_bin += [(guess, entropy)]
        
        if not best_flag:
            print(print_str)

    entropy_bin.sort(key=lambda x: x[1], reverse=True)
    best = [x for x in entropy_bin if x[1] == entropy_bin[-1][1]]

    print("Best guess(es): ")
    for (guess, entropy_val) in best:
        print(f"* {guess} [{entropy_val}]")
        for template in g_dict[guess]:
            print(f".... {template}:  {', '.join(g_dict[guess][template])}")
        
def main():
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
            find_entropies(guess_dict, best_flag=best_flag)
    
    
if __name__ == '__main__':
    main()