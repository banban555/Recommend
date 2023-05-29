import pandas as pd
from tabulate import tabulate
import sys
from utils import profile_function
from utils import timed_function
from db_connector import connect_to_db, fetch_all_data_from_table, fetch_data_for_user
from data_preprocessing import preprocess_data
from hashtag_analysis import create_hashtag_list, calculate_hashtag_weight, create_hashtag_representation, create_hashtag_similarity, get_user_dataframes, recommend_items
import time


def main(user_id):
    recommended = []
    cur = connect_to_db()
    preference_df = fetch_data_for_user(cur, user_id)

    user_records = fetch_data_for_user(cur, user_id)['record_id'].tolist()

    if not user_records:
        return recommended

    else:
        res = fetch_all_data_from_table(cur)
        prototypeData = pd.DataFrame.from_records(
            res, columns=[desc[0] for desc in cur.description])
        hashtag_df = preprocess_data(prototypeData)

        hashtag_list = create_hashtag_list(hashtag_df)
        hashtag_weighting = calculate_hashtag_weight(hashtag_df, hashtag_list)
        hashtag_representation = create_hashtag_representation(
            hashtag_df, hashtag_weighting)
        hashtag_similarity = create_hashtag_similarity(hashtag_representation)

        recommended = recommend_items(
            hashtag_similarity, user_records, n_recommendations=5)
        return recommended


# def main(user_id):
#     recommended = []

#     start_time = time.time()
#     cur = connect_to_db()
#     print("connect_to_db took: ", time.time() - start_time, " seconds")

#     start_time = time.time()
#     res = fetch_all_data_from_table(cur)
#     print("fetch_all_data_from_table took: ",
#           time.time() - start_time, " seconds")

#     start_time = time.time()
#     prototypeData = pd.DataFrame.from_records(
#         res, columns=[desc[0] for desc in cur.description])
#     print("Dataframe creation took: ", time.time() - start_time, " seconds")

#     start_time = time.time()
#     bookmark_df = fetch_data_for_user(cur, 'bookmark', user_id)
#     print("fetch_data_for_user for bookmarks took: ",
#           time.time() - start_time, " seconds")

#     start_time = time.time()
#     like_df = fetch_data_for_user(cur, 'likes', user_id)
#     print("fetch_data_for_user for likes took: ",
#           time.time() - start_time, " seconds")

#     start_time = time.time()
#     user_df = get_user_dataframes(bookmark_df, like_df)
#     print("get_user_dataframes took: ", time.time() - start_time, " seconds")

#     start_time = time.time()
#     user_records = list(user_df['record_id'])
#     print("list creation from user_df took: ",
#           time.time() - start_time, " seconds")

#     if not user_records:
#         return recommended
#     else:
#         start_time = time.time()
#         hashtag_df = preprocess_data(prototypeData)
#         print("preprocess_data took: ", time.time() - start_time, " seconds")

#         start_time = time.time()
#         hashtag_list = create_hashtag_list(hashtag_df)
#         print("create_hashtag_list took: ",
#               time.time() - start_time, " seconds")

#         start_time = time.time()
#         hashtag_weighting = calculate_hashtag_weight(hashtag_df, hashtag_list)
#         print("calculate_hashtag_weight took: ",
#               time.time() - start_time, " seconds")

#         start_time = time.time()
#         hashtag_representation = create_hashtag_representation(
#             hashtag_df, hashtag_list, hashtag_weighting)
#         print("create_hashtag_representation took: ",
#               time.time() - start_time, " seconds")

#         start_time = time.time()
#         hashtag_similarity = create_hashtag_similarity(hashtag_representation)
#         print("create_hashtag_similarity took: ",
#               time.time() - start_time, " seconds")

#         start_time = time.time()
#         recommended = recommend_items(
#             hashtag_similarity, user_records, n_recommendations=5)
#         print("recommend_items took: ", time.time() - start_time, " seconds")

#         return recommended


if __name__ == "__main__":
    user_id = sys.argv[1]
    recommended = main(user_id)
    print(recommended)
