from os import listdir, remove

def get_files(keywords):
    for filename in listdir('J:/scheduler/events/todo/'):
        if all(word in filename.lower() for word in keywords):
            yield filename

files = list(get_files(raw_input().lower().split()))
assert len(files) == 1

remove('J:/scheduler/events/todo/' + files[0])
