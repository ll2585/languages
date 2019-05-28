from konlpy.tag import Twitter
from languages import get_root
import time
import numpy as np
twitter = Twitter()
word = u'이것도'
twitter_times = []
trials = 10
for i in range(trials):
	t0 = time.time()
	print(twitter.stem(word))
	t1=time.time()
	time_taken = t1-t0
	twitter_times.append(time_taken)

print("Average twitter time: {0}".format(np.mean(twitter_times)))

my_times = []
t0 = time.time()
print(get_root(word))
t1=time.time()
print(t1-t0)