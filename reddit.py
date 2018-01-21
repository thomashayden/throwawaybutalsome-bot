import praw
import pickle
import time

import cred

reddit = praw.Reddit(client_id=cred.client_id,
                     client_secret=cred.secret,
                     username=cred.username,
                     password=cred.password,
                     user_agent=cred.user_agent)

neu = reddit.subreddit("NEU")

try:
    data = pickle.load(open("data.pkl", "rb"))
    print("Loaded file correctly")
except (OSError, IOError) as e:
    data = []
    pickle.dump(data, open("data.pkl", "wb"))
    print("Unable to load file. Created new one.")

start_time = time.time()

new_neu = neu.new()

for submission in new_neu:
    #print(submission.title)
    for comment in submission.comments:
        if comment.author == "throwawaybutalsome":
            for line in comment.body.split("\n"):
                if not line == "":
                    if not data.__contains__(line):
                        data.append(line)
                        print("Added " + line)
                    else:
                        print("Found duplicate")
    if time.time() - start_time > 60 * 10: # Run for 10 minutes, then break
        break
    time.sleep(2)  # The API is limited to 30 every minute, so there is a 2 second wait between each call

with open('data.pkl', 'wb') as f:
    pickle.dump(data, f)
    print("Saved data")