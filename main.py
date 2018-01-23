import pickle
import sys
import praw
import time
import datetime

import cred
from reddit import pull_reddit

from markov_chain import markov_chain

reddit = praw.Reddit(client_id=cred.client_id,
                     client_secret=cred.secret,
                     username=cred.username,
                     password=cred.password,
                     user_agent=cred.user_agent)

neu = reddit.subreddit("NEU")

while True:
    print("Starting search loop")
    rd = pull_reddit()

    try:
        with open("data.pkl", "rb") as f:
            data = pickle.load(f)
            print("Loaded markov data successfully")
    except (OSError, IOError) as e:
        print("Unable to markov data file. Try manually running reddit.py before running this.")
        sys.exit()

    better_data = []
    for dat in data:
        better_data.append(dat.split())
    mc = markov_chain(better_data)

    for posts in neu.new(limit=10):
        should_post = False;
        for comment in posts.comments:
            if comment.author == "throwawaybutalsome":
                should_post = True
        if not should_post:
            continue
        try:
            with open("posted.pkl", "rb") as f:
                posted = pickle.load(f)
                print("Loaded posted.pkl successfully!")
        except (OSError, IOError) as e:
            print("Unable to load posted.pkl. Creating file.")
            posted = []
            with open("posted.pkl", "wb") as f:
                pickle.dump(posted, f)

        url = "https://reddit.com" + posts.permalink

        if url not in posted:
            line = mc.generate_line()

            line = mc.generate_line()
            print(line)

            post_body = line + """
    ***
    *^Beep ^Boop. ^I'm ^a ^bot ^that ^uses ^markov ^chains ^to ^imitate ^the ^annoying ^comments ^of ^throwawaybutalsome.*
    *^Unless ^people ^actually ^like ^me^for^some^reason ^, ^I ^will ^only ^comment ^on ^a ^few ^posts ^before ^disappearing ^forever.*"""




            print("Replying")
            posts.reply(post_body) # API Call
            print("Replied with: " + post_body)
            print("Time is: " + str(datetime.datetime.now()))
            print("Sleeping for 12 minutes")
            posted.append(url)
            with open('posted.pkl', 'wb') as f:
                pickle.dump(posted, f)
                print("Saved data")
            print("Sleeping")
            time.sleep(60 * 12)
        print("Finished analyzing " + url)
    print("End of search loop. Sleeping for a while. Current time: " + str(datetime.datetime.now()) + ".\n Resume time should be: " + str(datetime.datetime.now() + datetime.timedelta(minutes=30)))
    time.sleep(60*30) # Wait 30 minutes and then check for more posts.