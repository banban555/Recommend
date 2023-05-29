import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
from utils import cos_sim_matrix, print_dictionary, remove_similar_item


def create_hashtag_list(hashtag_df):
    num_of_course = len(hashtag_df)
    hashtag_list = []
    for tags in hashtag_df['tag_name']:
        hashtag_list += tags.split(' ')
        hashtag_list = list(set(hashtag_list))
        hashtag_list = remove_similar_item(hashtag_list)
    return hashtag_list


def calculate_hashtag_weight(hashtag_df, hashtag_list):
    num_of_course = len(hashtag_df)
    hashtag_weighting = dict.fromkeys(hashtag_list)
    for each_hashtag in hashtag_df['tag_name']:
        for tag in each_hashtag.split(' '):
            tag = tag.strip()
            if tag in hashtag_weighting:
                if hashtag_weighting[tag] == None:
                    hashtag_weighting[tag] = 1
                else:
                    hashtag_weighting[tag] = hashtag_weighting[tag]+1
            else:
                continue

    for each_hashtag in hashtag_weighting:
        hashtag_weighting[each_hashtag] = np.log10(
            num_of_course/hashtag_weighting[each_hashtag])
    return hashtag_weighting


def create_hashtag_representation(hashtag_df, hashtag_weighting):
    hashtag_df.set_index('record_id', inplace=True)
    exploded_df = hashtag_df['tag_name'].str.split(' ', expand=True).stack()
    exploded_df = exploded_df.map(hashtag_weighting).fillna(0)
    exploded_df = exploded_df.reset_index(level=-1, drop=True)
    hashtag_representation = pd.pivot_table(exploded_df.to_frame(
    ), index=exploded_df.index, columns=exploded_df, fill_value=0)
    hashtag_representation.columns = hashtag_representation.columns.droplevel()

    return hashtag_representation


def create_hashtag_similarity(hashtag_representation):
    hashtag_similarity = cos_sim_matrix(
        hashtag_representation, hashtag_representation)
    # Set the columns to be the same as the index
    hashtag_similarity.columns = hashtag_representation.index
    return hashtag_similarity


def get_user_dataframes(user_df):
    user_df = user_df.drop_duplicates(subset=['user_id', 'record_id'])
    return user_df


def recommend_items(hashtag_similarity, user_records, n_recommendations=5):
    recommended = []
    user_similarities = hashtag_similarity.loc[user_records].sort_index()
    for idx in user_similarities.index:
        col = idx[0]
        user_similarities.loc[idx, col] = 0

    user_similarities = user_similarities.stack()

    while len(recommended) < n_recommendations:
        top_similarities = user_similarities.nlargest(1)
        index1 = top_similarities.index[0][0]
        index2 = top_similarities.index[0][1]
        if index2 not in recommended:
            recommended.append(index2)
        user_similarities[index1][index2] = 0
    return recommended
