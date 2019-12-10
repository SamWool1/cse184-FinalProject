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

delawareCities_raw = open('delaware_cities.txt')
delawareCities = delawareCities_raw.read().upper().split("\n")

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
    # del df['File Date']
    # del df['Patent Date']

    # Uppercase assignee names
    df['Assignee Name'] = df['Assignee Name'].apply(lambda x: str(x).upper())

    # Add column for field and field letter
    df['Fields'] = df['Fields'].str.get(0)
    df['CPC Category'] = df['Fields'].map(fieldTypes)

    # Parse location
    locations_raw = df['Assignee Location']
    locations = []
    for location in locations_raw:
        location = location.upper().split(', ')
        if len(location) == 1 or (len(location[0]) == 2 and location[0].isupper()):
            locations.append(location[0][0:2])
        else:
            if location[0] in delawareCities and location[1][0:2] == 'DE':
                locations.append(location[1][0:2] + ' (US)')
            else:
                locations.append(location[1][0:2])

    df['Assignee Location'] = locations
    print(df.head())
    df.to_csv('field_location_patents.csv')

createLocFieldSheet()
