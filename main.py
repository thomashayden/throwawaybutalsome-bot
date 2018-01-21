import pickle
import sys

from markov_chain import markov_chain

try:
    data = pickle.load(open("data.pkl", "rb"))
    print("Loaded file successfully")
except (OSError, IOError) as e:
    print("Unable to load file. Run reddit.py before running this.")
    sys.exit()

better_data = []
for dat in data:
    better_data.append(dat.split())

mc = markov_chain(better_data)
print(mc.generate_line())