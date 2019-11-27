# ---------------------------------------------------------------------------
# Using a random sample of patent numbers, scrapes the data using pypatent
# and creates a .csv based on the scraped data.
# ---------------------------------------------------------------------------

from PatentWithField import PatentWithField
import time
import pandas as pd

applicationTypes = {

}

fieldTypes = {
    'A': 'Human Necessities',
    'B': 'Performing Operations, Transporting',
    'C': 'Chemistry, Metallurgy',
    'D': 'Textiles, Paper',
    'E': 'Fixed Construction',
    'F': 'Mechanical Engineering, Lighting, Heating, Weapons, Blasting Engines or Pumps',
    'G': 'Physics',
    'H': 'Electricity',
    'Y': 'General New Technological Developments',
}

# Generates a URL corresponding a specific patent - used in scraping


def generatePatentURL(patnum):
    return ("http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2"
            "=HITOFF&u=%%2Fnetahtml%%2FPTO%%2Fsearch-adv.htm&r=1&p=1&f="
            "G&l=50&d=PTXT&S1"
            "=%s.PN.&OS=PN/%s&RS=PN/%s" % (patnum, patnum, patnum))


# Returns the sampled patent numbers as a list
def getSamples(filename, year):
    print('Reading samples')
    f = open(filename + year + '.txt', 'r')
    str_samples = f.readline()
    print('Read samples')
    samples = str_samples.split(', ')
    return samples


# Returns the patent as a dictionary. Built-in method causes issues and
# includes unneeded information (abstract)
def getPatentAsDict(p):
    d = {}
    d['Applicant Country'] = p.applicant_country

    # Get first 2 digits of application number to get application type TODO remove because better way exists
    try:
        d['Applicant Number '] = p.applicant_num.split('/')[0]
    except Exception:
        d['Applicant Number'] = 'Unknown'

    d['Assignee Name'] = p.assignee_name
    d['File Date'] = p.file_date
    d['Patent Date'] = p.patent_date
    d['Patent Number'] = p.patent_num
    d['Title (Patent Number)'] = p.title

    # Gets most valid CPC field for this patent
    try:
        fields_raw = p.fields.split('; ')
        fields = {}
        for field_raw in fields_raw:
            field = field_raw[0]
            if field in fields:
                fields[field] = fields[field] + 1
            else:
                fields[field] = 1
        field = max(fields, key=fields.get)
        try:
            d['Fields'] = fieldTypes[field]
        except Exception:
            d['Fields'] = field

    except Exception:
        d['Fields'] = 'Unknown'

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
        try:
            p.fetch_details()
        except:
            print('Fetch for ' + str(sample) + ' failed')
            
        print('Fetched number ' + sample)
        p_dict = getPatentAsDict(p)

        if df is None:
            df = pd.DataFrame([p_dict])
        else:
            temp = pd.DataFrame([p_dict])
            df.loc[i] = temp.loc[0]
    return df


def main():
    year = str(2018)
    samples = getSamples('samples/sample_numbers', year)
    df = getDataframe(samples)
    df.to_csv('scrapes/scraped_patents' + year + '.csv')
    print('CSV created')


main()
