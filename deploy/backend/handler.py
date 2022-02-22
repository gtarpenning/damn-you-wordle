import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import uuid
import logging

from wordle_assistant import *


# Globals to load on server spinup
answers, allowed = load_word_lists()
candidate_lookup, template_lookup = load_lookup_tables()


def wordle_request(w_request):
    """ Main function for handling a request to the wordle request endpoint
        accepts a WorldeRequest object and returns json, with an error
        message on error, otherwise with a prompt to continue wordling 
    """
    guess = w_request.guess
    template = w_request.template
    answers_left = w_request.answers_left
    allowed_left = w_request.allowed_left

    if not answers_left or allowed_left:
        answers_left = candidate_lookup[guess][template]
        allowed_left = narrow_down(guess, template, allowed.copy(), template_lookup)
    
    best_guesses = find_entropies(answers_left, allowed_left, candidate_lookup)

    out = {
        "best_guess": best_guesses[0][0] if len(best_guesses) > 0 else [],
        "answers_left": answers_left,
        "allowed_left": allowed_left,
    }

    print(f"Returning to endpoint: {out}")

    return out


def cloud_endpoint_request():
    """
    make_authorized_get_request makes a GET request to the specified HTTP endpoint
    in service_url (must be a complete URL) by authenticating with the
    ID token obtained from the google-auth client library.
    """
    # local dev imports
    import urllib

    import google.auth.transport.requests
    import google.oauth2.id_token
    
    # hardcoded, only one endpoint to test
    service_url = 'https://damn-you-wordle-uykoh7fkza-uw.a.run.app/'

    req = urllib.request.Request(service_url)

    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, service_url)

    req.add_header("Authorization", f"Bearer {id_token}")
    response = urllib.request.urlopen(req)

    return response.read()