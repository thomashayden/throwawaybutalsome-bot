# throwawaybutalsome-bot
A reddit bot designed to emulate the questionably hillarious antics of /u/throwawaybutalsome

## How it works
When the program is run, it first pulls all comments from /u/throwawaybutalsome and saves them to a file. It then loads the comments into a markov chain object, which can then generate sentences that sound (somewhat) like him. The program then looks through the most recent 10 reddit posts on /r/NEU and checks to see if both the bot has not yet posted there, and /u/throwawaybutalsome has already posted there (this is to make sure the bot only posts on the already tainted posts). If it finds a suitable place to post, it posts a random sentence and sleeps for 12 minutes (as not to annoy the reddit api). When it has gone through the 10 most recent posts, it sleeps for 30 minutes to wait for new posts and does everything all over again. Thus is the never ending cycle of life. Pointless and annoying to the average redditor.
