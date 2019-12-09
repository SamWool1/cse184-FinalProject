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

    # test_func(df)


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
    print('line_df:')
    print(line_df.head())
    line_df.to_csv('lineChartData.csv')

    df = pd.read_csv('lineChartData.csv')
    print('df:')
    print(df.head())
    df = df.drop(df.columns[0], axis=1)
    print(df.head())
    df = df.set_index('Year')
    print(df.head())
    df = df.cumsum()
    print(df.head())
    df.to_csv('lineChartData.csv')

def makeLineDf(year):
    df = pd.read_csv('scrapes/scraped_patents' + year + '.csv')
    df.dropna(subset=['Assignee Name'], inplace=True)

    assignee_name_df = getCountAndPercent(df.loc[:, 'Assignee Name'])
    assignee_name_df['Year'] = year
    print('Finished ' + year)
    return(assignee_name_df.sort_values('Count', ascending=False).head())

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
        fields.append(mf.iloc[rowNum, 8])
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

# makeLineCSV()
makeRacingBar()
makeBarCumSum()
createUnifiedScrape()
# for year in range(1980, 2019):
#     print('Wrangling ' + str(year))
#     main(str(year))
#     input('Finished ' + str(year) + ', press Enter to continue...')
# print('All wrangling finished')
