import sys

import spam

import spam.email

from spam import email

from spam.email import send_spam_email as not_spam

from spam import *

def print_spam():
    print('Sending spam...')
    print('-'*40)
    spam.email.send_spam_email()
    print('-'*40)
    print(__name__)
    # spam.send_definitely_not_spam_email()
    # print(dir(spam))
    # print(spam.__path__)
    # print(spam.version)

if __name__ == '__main__':
    print_spam()
    print(sys.path)