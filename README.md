Purdue class watcher
====================
This is a simple Ruby script which will hit myPurdue and check if there are any open seats for a given class. 
Edit the source to specify your [instapush.im](http://instapush.im) information, or comment it out to disable it.

Installation
============
1. Download the script. Install the gems `nokogiri` and `instapush`.
2. Create an [instapush.im](http://instapush.im) account.
3. Install the instapush client on your mobile device.
4. Go to your Dashboard and select Apps.
5. Add an application and name it whatever you like.
6. Add an event named `open-seats` with trackers `course` and `seats`. You can customize the message as you like:
   that part is what will go to your phone.
7. Go to the Basic Info tab and take note of the app's ID and secret.
8. Modify [`main`](main)'s line #25 to use your application ID and secret.

Usage
=====
Run the script as follows:

    ruby main -c CRN -t TERM

Note: For fall 2015, the "term" is 201610. So, if I were to query for open seats in ECON451: Game Theory for next 
semester, I would run the following:

    ruby main -c 53454 -t 201610
