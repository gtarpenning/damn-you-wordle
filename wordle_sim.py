

# class Wordle:
#     def __init__(self, epochs=1):
#         self.allowed = []
#         with open("./wordle-allowed-guesses.txt", "r") as f:
#             self.allowed = f.read().split('\n')	

#         self.answers = []
#         with open("./wordle-answers-alphabetical.txt", "r") as f:
#                 self.answers = f.read().split('\n')

#         print(f"Initializing sim ({len(self.answers)} words) with {epochs} epochs (default 1)")
#         self.epochs = epochs

#     def do_all_games(self, word):
#         score_history = []  # contains board history

#         for guess in self.allowed:
#             # guess_history += [guess]
#             score_history += [self.do_turn(word, guess)]
#             if score_history[-1] == "XXXXX":  # done
#                 break

#     def do_turn(self):
#         pass

#     def get_stats(self):
#         pass