# ---------------------------------------------------------------------------
# Generates a random sample of 100 unique patent numbers for scraping
# Will be increased to around 1000, possibly higher
# ---------------------------------------------------------------------------

import random

sample_size = 100
sample = random.sample(range(310999), sample_size)
sample.sort()
sample = [x + 9854721 for x in sample]

str_sample = str(sample)
str_sample = str_sample[1:len(str_sample)-1]

f = open('sample_numbers.txt', 'w')
f.write(str_sample)
f.close()