import pandas as pd


def clean_api_text(api_text):
    api_rows = api_text.split()
    api_rows[0] = api_rows[0][2:-2]
    for i in range(1, len(api_rows) - 1):
        api_rows[i] = api_rows[i][1:-2]
    api_rows[-1] = api_rows[-2][1:-2]
    api_rows = [x.split(',') for x in api_rows]
    for i in range(len(api_rows)):
        api_rows[i] = [val.replace('"', '') for val in api_rows[i]]
    return pd.DataFrame(api_rows[1:], columns=api_rows[0])
    