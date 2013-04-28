""" Based on https://gist.github.com/2633554 """
import email
import getpass, imaplib
import os

def download(query, username, password=None, directory=None):
    """
    Downloads all attachments from emails that match the given search query.
    Logs into GMail using the provided username and password.
    By default the target directory to where the attachments are saved is the
    localized desktop, and downloads the attachments from only one email.
    Only emails younger than 6 months are returned.
    If a password is not provided, one will be requested from the user.

    Returns the path of the files downloaded.
    """
    if not directory:
        try:
            # Windows desktop location. Note that in localized system this may
            # not be the exact string "Desktop", but something like "Area de
            # Trabalho".
            from win32com.shell import shell, shellcon
            directory = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, 0, 0)
        except:
            # Fallback for Unix and OSX.
            directory = '~/Desktop'

    # Add attachment and read restrictions to the query. No point in searching
    # emails without attachment or that the user hasn't read yet.
    full_search_query = query + ' has:attachment is:read newer_than:6m'

    if not password:
        password = getpass.getpass('Password: ')

    imap_session = imaplib.IMAP4_SSL('imap.gmail.com')
    result, account_details = imap_session.login(username, password)
    assert result == 'OK'

    imap_session.select('[Gmail]/All Mail')
    # X-GM-RAW tells the imap session to use GMail's search system, not the
    # built-in one.
    result, data = imap_session.search(None, 'X-GM-RAW', full_search_query)
    assert result == 'OK'

    downloads = []

    # The messages are returned in order from oldest to newest. We must revert
    # this order and get only the number of messages required.
    message_id = data[0].split()[-1]
    result, messageParts = imap_session.fetch(message_id, '(RFC822)')
    assert result == 'OK'

    email_body = messageParts[0][1]
    mail = email.message_from_string(email_body)

    for part in mail.walk():
        # Ignore containers.
        if (part.get_content_maintype() == 'multipart' or
            part.get('Content-Disposition') is None):
            continue

        filename = part.get_filename()
        path = os.path.join(directory, filename)
        with open(path, 'wb') as file:
            downloads.append(path)
            file.write(part.get_payload(decode=True))

    imap_session.close()
    imap_session.logout()

    return downloads

import tarfile
from zipfile import ZipFile
from os import remove

def extract_type(function, path):
    directory = '/'.join(path.split('/')[:-1])
    with function(path) as compressed_file:
        compressed_file.extractall(directory)
    remove(path)

def try_extract(path):
    if path.endswith('tar') or file.endswith('gz') or file.endswith('bz2'):
        extract_type(tarfile.open, path)
    elif path.endswith('zip'):
        extract_type(ZipFile, path)


if __name__ == '__main__':
    for path in download(raw_input(), 'lucasboppre'):
        try_extract(path)
