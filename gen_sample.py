# ---------------------------------------------------------------------------
# Generates a random sample of 100 unique patent numbers for scraping
# Will be increased to around 1000, possibly higher
# ---------------------------------------------------------------------------

import random

patent_num_start = {
    '1980': 4180867,
    '1981': 4242757,
    '1982': 4308622,
    '1983': 4366579,
    '1984': 4423523,
    '1985': 4490855,
    '1986': 4562596,
    '1987': 4633526,
    '1988': 4716594,
    '1989': 4794652,
    '1990': 4890335,
    '1991': 4980927,
    '1992': 5077836,
    '1993': 5175886,
    '1994': 5274846,
    '1995': 5377359,
    '1996': 5479658,
    '1997': 5590420,
    '1998': 5704062,
    '1999': 5855021,
    '2000': 6009555,
    '2001': 6167569,
    '2002': 6334220,
    '2003': 6502244,
    '2004': 6671884,
    '2005': 6836899,
    '2006': 6981282,
    '2007': 7155746,
    '2008': 7313829,
    '2009': 7472428,
    '2010': 7640598,
    '2011': 7861317,
    '2012': 8087094,
    '2013': 8341762,
    '2014': 8621662,
    '2015': 8925112,
    '2016': 9226437,
    '2017': 9532496,
    '2018': 9854721,
    '2019': 10165721
}

patent_num_amt = {}

for i in range(1980, 2019):
    patent_num_amt[str(i)] = patent_num_start[str(i + 1)] - \
        patent_num_start[str(i)] - 1


def sampleByYear(year):
    sample_size = 100
    sample = random.sample(range(patent_num_amt[year]), sample_size)
    sample.sort()
    sample = [x + patent_num_start[year] for x in sample]

    str_sample = str(sample)
    str_sample = str_sample[1:len(str_sample)-1]

    f = open('samples/sample_numbers' + year + '.txt', 'w')
    f.write(str_sample)
    f.close()
    print('Samples for ' + year + ' generated')


for i in range(1980, 2019):
    sampleByYear(str(i))