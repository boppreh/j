j
=

Background application that listen for global hotkeys and run the
corresponding scripts.

Whenever the user presses Alt+Letter (in any program), J internally navigates
to the first file or folder that starts with that letter. When it reaches a
deadend or has finished executing a script, it goes back to its root.

The scripts can have any extension, are only loaded when you use their hotkey
and are not cached between executions.


Example
-------

- global_j.pyw
- search/
- search/google.py
- search/clipboard/
- search/clipboard/google.py

If you press Alt+S, Alt+G it'll run 'search/google.py'.
If you press Alt+S, Alt+C, Alt+G it'll run 'search/clipboard/google.py'.
