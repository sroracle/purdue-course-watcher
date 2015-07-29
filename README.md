Purdue class watcher
====================
This is a simple Python script which will hit myPurdue and check if there are any open seats for a given class. 

Installation
============
1. Install `beautifulsoup4` for Python 3.
2. Download the script.
3. Optionally, move `push.py` to `/usr/local/bin` and edit `/etc/push.py.ini` like the given `push.py.ini`.
4. Enjoy!

Usage
=====
Run the script as follows:

    python main.py TERM CRN

Note: For fall 2015, the "term" is 201610. So, if I were to query for open seats in ECON451: Game Theory for next 
semester, I would run the following:

    python main.py 201610 53454

`push.py` can also be used as a standalone script, as in the following:

    echo 'Message this to my phone' | ./push.py
