# ---------------------------------------------------------------------------
# Parse and wrangle fields and locations specifically
# ---------------------------------------------------------------------------

import pandas as pd
import numpy as np
import datetime

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

# Creates a single spreadsheet with values for all years
def createLocFieldSheet():
    df = pd.DataFrame()
    for year in range(1980, 2019):
        year = str(year)
        temp = pd.read_csv('scrapes/scraped_patents' + year + '.csv')
        temp['Year'] = year
        df = df.append(temp)

    # Drop NaN
    df.dropna(subset=['Assignee Name', 'Fields', 'Assignee Location'], inplace=True)

    # Drop extraneous fields
    del df['Unnamed: 0'] # what is this?
    del df['Applicant City']
    del df['Applicant Country']
    del df['Applicant Number']
    del df['Applicant State']
    del df['Inventors']
    del df['Family Id']
    del df['File Date']
    del df['Patent Date']

    # Uppercase assignee names
    df['Assignee Name'] = df['Assignee Name'].apply(lambda x: str(x).upper())

    # Assign corresponding CPC category for each field
    for i, row in df.iterrows():
        print(row['Fields'] + ' ' + str(i))

    print(df.head())

createLocFieldSheet()