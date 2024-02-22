import pandas as pd
import uuid
import json

# File paths
CSV_DATA = '../data/linkedin_canada.csv'
CSV_DATA_FINAL = '../data/dataset.csv'
JSON_TITLES = '../dictionaries/titles.json'
JSON_SECTORS = '../dictionaries/sectors.json'

# Load the dataframe
df = pd.read_csv(CSV_DATA)

# Create column "id"
df['id'] = [uuid.uuid4() for _ in range(df.shape[0])]
assert 'id' in df.columns.to_list(), 'Error: "id" not added to columns.'

# Remove "salary" column
df.drop(columns=['salary'], inplace=True)
assert 'salary' not in df.columns.to_list(), 'Error: "salary" not removed from columns.'

# Remove rows with null values
df.dropna(inplace=True)
assert df.isna().sum().sum() == 0, 'Error: There are still missing values.'

# Filter the dataframe to the year 2024
df['publishedAt'] = pd.to_datetime(df['publishedAt'])
df = df[df['publishedAt'].dt.year == 2024]
assert (df['publishedAt'].dt.year == 2024).all(), 'Error: There are values that are not from the year 2024.'

# Replaces the values of "title" according to the json file
with open(JSON_TITLES, 'r', encoding='utf-8') as file:
    titles_dict = json.load(file)
    df['title'].replace(titles_dict, inplace=True)
    assert set(df['title'].unique()) == set(titles_dict.values()), 'Error: Not all "title" values were converted correctly.'

# Replaces the values of "sector" according to the json file
with open(JSON_SECTORS, 'r', encoding='utf-8') as file:
    sector_dict = json.load(file)
    df['sector'].replace(sector_dict, inplace=True)
    assert set(df['sector'].unique()) == set(sector_dict.values()), 'Error: Not all "sector" values were converted correctly'

# Saves the dataframe data to a new file
df.to_csv(CSV_DATA_FINAL, index=False)
