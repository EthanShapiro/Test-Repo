import httplib2
import os
from bs4 import BeautifulSoup
import bs4.element
import re
import string

from apiclient import discovery, errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import base64
import email

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = ('https://www.googleapis.com/auth/gmail.readonly', "https://www.googleapis.com/auth/gmail.modify")
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_message(service, user_id, msg_id):
    """Get a Message with given ID.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The ID of the Message required.

    Returns:
        A Message.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        print('Message snippet: %s' % message['snippet'])

        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def get_mime_message(service, user_id, msg_id):
    """Get a Message and use it to create a MIME Message.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The ID of the Message required.

      Returns:
        A MIME Message, consisting of data from Message.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id,
                                                 format='raw').execute()

        print('Message snippet: %s' % message['snippet'])

        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

        mime_msg = email.message_from_string(msg_str.decode("ASCII"))

        return mime_msg
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

hw_assigments = {}
def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().messages().list(userId="me", q="from:(system@schoolloop.com)").execute()
    ids = results.get('messages', [])

    message = get_message(service, 'me', ids[1]['id'])
    # print(message['payload']['parts'][1]["body"]["data"])
    msg_html = base64.urlsafe_b64decode(message['payload']['parts'][1]["body"]["data"].encode('ASCII'))
    soup = BeautifulSoup(msg_html, 'lxml')
    table = soup.find('td', text="Due:").parent.parent
    fulstrings = []

    for child in table.children:
        if type(child) != bs4.element.NavigableString:
            for c in child.children:
                if not c.string:
                    continue
                fulstrings.append(c.string)
    for i, word in enumerate(fulstrings):
        fulstrings[i] = format_homework(word)
    hw = ' '.join(filter(lambda x: x, fulstrings))
    days = ["Sun:", "Mon:", "Tue:", "Wed:", "Thu:", "Fri:", "Sat:"]
    re_match = list(map(lambda x: re.search(x, hw), days))
    for i, result in enumerate(re_match):
        if i+1 < len(days):
            hw_assigments[days[i]] = hw[result.span()[1]:re_match[i+1].span()[0]]
        else:
            hw_assigments[days[i]] = hw[result.span()[1]:]
    print(hw_assigments)


def format_homework(old_str):
    old_str = re.sub('[ ]+', ' ', old_str)
    new_str = ''.join(filter(lambda x: x in string.printable, old_str))
    new_str = re.sub('[\t\n\r\f\v]+', '', new_str)
    return new_str.strip()


if __name__ == '__main__':
    main()