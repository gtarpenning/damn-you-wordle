import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


import logging


def init_db_handler():
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


def wordle_request(w_request):
    """ Main function for handling a request to the wordle request endpoint
        accepts a WorldeRequest object and returns json, with an error
        message on error, otherwise with a prompt to continue worlding 
    """
    return None


def main():
    db = init_db_handler()
    get_users(db)


if __name__ == "__main__":
    main()
