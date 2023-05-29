import re
import pandas as pd


def remove_non_korean(x):
    x = re.sub('[^가-힣a-zA-Z0-9\s]', '', x)
    return None if x.strip() == '' else x


def preprocess_data(prototypeData):
    hashtag_df = prototypeData[['record_id', 'tag_name']]
    hashtag_df = hashtag_df.groupby('record_id')['tag_name'].apply(
        lambda x: ' '.join(x)).reset_index()
    hashtag_df['tag_name'] = hashtag_df['tag_name'].str.replace(
        "[^가-힣\s]", "", regex=True)
    hashtag_df = hashtag_df.dropna()
    return hashtag_df
