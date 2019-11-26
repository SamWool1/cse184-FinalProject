# ---------------------------------------------------------------------------
# Using a random sample of patent numbers, scrapes the data using pypatent
# and creates a .csv based on the scraped data.
# ---------------------------------------------------------------------------

from PatentWithField import *
import time
import pandas as pd

# Generates a URL corresponding a specific patent - used in scraping


def generatePatentURL(patnum):
    return ("http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2"
            "=HITOFF&u=%%2Fnetahtml%%2FPTO%%2Fsearch-adv.htm&r=1&p=1&f="
            "G&l=50&d=PTXT&S1"
            "=%s.PN.&OS=PN/%s&RS=PN/%s" % (patnum, patnum, patnum))


# Returns the sampled patent numbers as a list
def getSamples(filename):
    print('Reading samples')
    f = open(filename, 'r')
    str_samples = f.readline()
    print('Read samples')
    samples = str_samples.split(', ')
    return samples


# Returns the patent as a dictionary. Built-in method causes issues and
# includes unneeded information (abstract)
def getPatentAsDict(p):
    d = {}
    d['Applicant City'] = p.applicant_city
    d['Applicant Country'] = p.applicant_country
    d['Applicant Number'] = p.applicant_num
    d['Applicant State'] = p.applicant_state
    d['Assignee Location'] = p.assignee_loc
    d['Assignee Name'] = p.assignee_name
    d['Family Id'] = p.family_id
    d['File Date'] = p.file_date
    d['Inventors'] = p.inventors
    d['Patent Date'] = p.patent_date
    d['Patent Number'] = p.patent_num
    d['Title (Patent Number)'] = p.title
    d['Fields'] = p.fields
    d['fetched'] = p.fetched_details
    return d


# Creates a DataFrame based on the scraped patents retrieved
def getDataframe(samples):
    df = None
    for i, sample in enumerate(samples):

        # Wait to get around forcible close from remote
        time.sleep(1)

        # TODO catch forcible close from remote (resolved by wait?)
        p = PatentWithField(title='#' + str(sample),
                            url=generatePatentURL(sample))
        print('Starting fetch of number ' + sample)
        p.fetch_details()
        print('Fetched number ' + sample)
        p_dict = getPatentAsDict(p)

        if df is None:
            df = pd.DataFrame([p_dict])
        else:
            temp = pd.DataFrame([p_dict])
            df.loc[i] = temp.loc[0]
    return df


def main():
    samples = getSamples('sample_numbers.txt')
    df = getDataframe(samples)
    df.to_csv(r'scraped_patents.csv')
    print('CSV created')


main()
