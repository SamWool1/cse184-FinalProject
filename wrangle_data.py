# ---------------------------------------------------------------------------
# Parse and wrangle data
# ---------------------------------------------------------------------------

import pandas as pd
import numpy as np
import datetime

# Creates a single spreadsheet with values for all years
def createUnifiedScrape():
    unified_df = pd.DataFrame()
    for year in range(1980, 2019):
        year = str(year)
        df = pd.read_csv('scrapes/scraped_patents' + year + '.csv')
        df['Year'] = year
        unified_df = unified_df.append(df)
    print(unified_df.head())
    unified_df.to_csv('unified_patents.csv')

# Get a count and percentage of unique values in a column
def getCountAndPercent(values):

    # Get number of occurrences for each value
    count_values = {}
    for value in values:
        value = str(value).upper()

        if value not in count_values:
            count_values[value] = 1
        else:
            count_values[value] = count_values[value] + 1

    # Craete dataframe and get percentage of appearances for each value
    total_count = len(values)
    df = pd.DataFrame(columns=np.arange(3))
    df.columns = ['Value', 'Count', 'Percentage']

    for i, value in enumerate(count_values):
        count = count_values[value]
        percentage = (count/total_count) * 100
        df.loc[i] = [value, count, percentage]

    return df

# TODO remove, for testing date-time delta stuff
def test_func(df):
    dates = df.loc[:, 'Patent Date']
    for date_str in dates:
        try:
            date = datetime.datetime.strptime(date_str, '%B %d, %Y')
            print(date)
        except Exception:
            print('Unknown')
    return

def main(year):
    df = pd.read_csv('scrapes/scraped_patents' + year + '.csv')
    df.dropna(subset=['Assignee Name'], inplace=True)

    assignee_name_df = getCountAndPercent(df.loc[:, 'Assignee Name'])
    print(assignee_name_df.sort_values('Count', ascending=False).head())

    place_df = getCountAndPercent(df.loc[:, 'Assignee Location'])
    print(place_df.sort_values('Count', ascending=False))

#Create a CSV for a line graph
def makeLineCSV():
    line_df = pd.DataFrame()

    for year in range(1980, 2019):
        year = str(year)
        line_df = line_df.append(makeLineDf(year))

    line_df = line_df.reset_index()
    line_df = line_df.drop(['Count', 'index'], axis=1)
    line_df = line_df.pivot(index='Value', columns='Year')
    line_df = line_df.dropna(thresh = 5)
    line_df = line_df.fillna(0)
    line_df = line_df.T
    line_df[line_df.columns[0:]] = line_df[line_df.columns[0:]] * 50
    line_df.to_csv('lineChartData.csv')

    df = pd.read_csv('lineChartData.csv')
    df = df.drop(df.columns[0], axis=1)
    df = df.set_index('Year')
    df = df.cumsum()
    df.to_csv('lineChartData.csv')

def makeLineDf(year):
    df = pd.read_csv('scrapes/scraped_patents' + year + '.csv')
    df.dropna(subset=['Assignee Name'], inplace=True)

    assignee_name_df = getCountAndPercent(df.loc[:, 'Assignee Name'])
    assignee_name_df['Year'] = year
    print('Finished ' + year)
    return(assignee_name_df.sort_values('Count', ascending=False).head())

def getTimeDiff():
    fields = [
        'Human Necessities',
        'Performing Operations, Transporting',
        'Chemistry, Metallurgy',
        'Textiles, Paper',
        'Fixed Construction',
        'Mechanical Engineering, Lighting, Heating, Weapons, Blasting Engines or Pumps',
        'Physics',
        'Electricity',
    ]
    dict = {}

    df = pd.read_csv('field_location_patents.csv')

    #delete unneeded columns
    del df['Unnamed: 0']
    del df['Assignee Location']
    del df['Fields']
    del df['Patent Number']
    del df['Title (Patent Number)']
    del df['fetched']

    #format the file date and patent date columns
    df['File Date'] = pd.to_datetime(df['File Date'], format="%B %d, %Y", errors='coerce')
    df['Patent Date'] = pd.to_datetime(df['Patent Date'], format="%B %d, %Y", errors='coerce')

    df['Time Difference'] = df['Patent Date'] - df['File Date']
    df.dropna()

    df.sort_values(by='CPC Category', inplace=True)
    df.set_index('CPC Category', inplace=True)

    #get average for each different Category and make new df
    for field in fields:
        a = {field: str(df.loc[field, 'Time Difference'].mean().days)}
        dict.update(a)
    ff = pd.DataFrame(list(dict.items()), columns=['Fields', 'Time Difference (days)'])
    ff.sort_values('Time Difference (days)', inplace=True)

    ff.to_csv('timeDiffFields.csv')

def makeRacingBarCountries():
    ddf = pd.DataFrame()
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

    df = pd.read_csv('field_location_patents.csv')

    #delete unneeded columns
    del df['Unnamed: 0']
    del df['Assignee Name']
    del df['Fields']
    del df['File Date']
    del df['Patent Date']
    del df['Patent Number']
    del df['Title (Patent Number)']
    del df['fetched']
    # del df['Year']

    df.sort_values(by='CPC Category', inplace=True)
    df.set_index('CPC Category', inplace=True)
    df.replace(to_replace=states, value = 'US', inplace=True)

    print(df)
    df.to_csv('asdsadasd.csv')

    for year in range(1980,2019):
        af = df.loc[df['Year'] == year]
        cf = getCountAndPercent(af.loc[:, 'Assignee Location']).sort_values('Count', ascending=False)
        del cf['Percentage']
        cf['Year'] = year
        ddf = ddf.append(cf)

    print(ddf)

    ddf = ddf.pivot(index='Value', columns='Year')
    ddf.dropna(thresh=20, inplace=True)
    ddf.fillna(0, inplace=True)
    ddf = ddf.cumsum(axis = 1)
    ddf = ddf.reset_index()
    print(ddf)

    ddf.to_csv('totalPatentCountCountry.csv')

def makeRacingBar():
    fields = []
    locations = []

    #format lineChartData for a racing bar chart
    df = pd.read_csv('lineChartData.csv')
    df = df.set_index('Year')

    #get all company names
    names = list(df.columns)

    df = df.T

    #get first occurence of company's name
    mf = pd.read_csv('field_location_patents.csv')
    for name in names:
        rowNums = mf.loc[mf['Assignee Name'] == name].index.tolist()
        rowNum = rowNums[0]
        fields.append(mf.iloc[rowNum, 10])
        locations.append(mf.iloc[rowNum, 1])

    df['Company Field'] = fields
    df['Company Location'] = locations

    #output a csv
    df.to_csv('racingBar.csv')

def makeBarCumSum():
    df = pd.read_csv('lineChartData.csv')
    year = 1980
    for row in range(0, 39):
        df.iloc[row].to_csv('barCharts/cumSum' + str(year) + '.csv')
        year = year + 1

makeRacingBarCountries()
#getTimeDiff()
# makeLineCSV()
#makeRacingBar()
# makeBarCumSum()
# createUnifiedScrape()
# for year in range(1980, 2019):
#     print('Wrangling ' + str(year))
#     main(str(year))
#     input('Finished ' + str(year) + ', press Enter to continue...')
# print('All wrangling finished')
