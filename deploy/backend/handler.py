import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import uuid
import logging

from wordle_assistant import *


def get_db_handler():
    """ Connect to the firebase db """
    # Use the application default credentials
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
      'projectId': 'damn-you-wordle',
    })

    db = firestore.client()
    return db


def get_users(db):
    """ Utility function to return all users from firebase """
    users_ref = db.collection(u'users')
    docs = users_ref.stream()
    for doc in docs:
        print(doc.to_dict())
        logging.info(f"User: {doc.to_dict()}")


def make_session_ID():
    """ Make Random Session ID to keep track of concurrent sessions """
    return str(uuid.uuid1())


def get_wordlists_for_session(db, sessionID):
    """ 
    Requests database for stored word lists, given a username
    If username has an active session with existing word lists, 
    those are returned, otherwise the default word lists returned
    """
    wordlists = db.collection(u'wordlists').document(sessionID).get()
    if not wordlists.exists:
        answers, allowed = load_word_lists()
        return answers, allowed, "No wordlist for sessionID"

    return wordlists.to_dict()['answers'], wordlists.to_dict()['allowed'], None


def store_wordlists_by_sessionID(answers_left, allowed_left, db, sessionID):
    """ Uses a sessionID as a key to store the two wordlists """
    wordlists = db.collection(u'wordlists').document(sessionID)
    wordlists.set({
        'answers': answers_left,
        'allowed': allowed_left,
    })
    logging.info(wordlists)


def wordle_request(w_request):
    """ Main function for handling a request to the wordle request endpoint
        accepts a WorldeRequest object and returns json, with an error
        message on error, otherwise with a prompt to continue wordling 
    """
    db = get_db_handler()

    guess = w_request.guess
    template = w_request.template

    answers_left, allowed_left, err = get_wordlists_for_session(db, w_request.sessionID)

    if err and err == "No wordlist for sessionID":
        sessionID = make_session_ID()
    
    answers_left = narrow_down(guess, template, answers_left)
    allowed_left = narrow_down(guess, template, allowed_left)

    store_wordlists_by_sessionID(answers_left, allowed_left, db, sessionID)
    
    guess_dict = make_guess_dict(allowed_left, answers_left)
    best_guesses = find_entropies(guess_dict, answers_left)

    return {
        "best_guesses": best_guesses,
        "sessionID": sessionID,
    }
    

def main():
    answers, allowed = load_word_lists()
    db = get_db_handler()
    
    # Admin method
    get_users(db)
    sID = make_session_ID()
    print(sID)
    get_wordlists_for_session(db, sID)


if __name__ == "__main__":
    main()
