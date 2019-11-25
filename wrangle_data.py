# ---------------------------------------------------------------------------
# Parse and wrangle data
# ---------------------------------------------------------------------------

import pandas as pd
import numpy as np
import datetime

# Get a count and percentage of unique values in a column


def getCountAndPercent(values):

    # Get number of occurrences for each value
    count_values = {}
    for value in values:

        if value not in count_values:
            count_values[value] = 1
        else:
            count_values[value] = count_values[value] + 1

    # Craete dataframe and get percentage of appearances for each value
    total_count = len(count_values)
    df = pd.DataFrame(columns=np.arange(3))
    df.columns = ['Value', 'Count', 'Percentage']

    for i, value in enumerate(count_values):
        count = count_values[value]
        percentage = count/total_count
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


def main():
    df = pd.read_csv('scraped_patents.csv')
    df.fillna('Unknown', inplace=True)
    assignee_name_df = getCountAndPercent(df.loc[:, 'Assignee Name'])
    print(assignee_name_df.head())

    # test_func(df)


main()
