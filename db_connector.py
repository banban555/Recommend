import pymysql
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()


def connect_to_db():
    conn = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=int(os.getenv('DB_PORT')),
        db=os.getenv('DB_NAME'),
        charset='utf8')
    cur = conn.cursor()
    return cur


def fetch_all_data_from_table(cursor):
    sql = """
    SELECT hashtag.id, hashtag.record_id, hashtag.tag_name, hashtag.hashtag_type
    FROM hashtag
    JOIN record ON hashtag.record_id = record.id
    WHERE record.deleted_at IS NULL
    """
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


def fetch_data_for_user(cursor, user_id):
    sql = f"""
    SELECT bookmark.user_id, bookmark.record_id 
    FROM bookmark
    JOIN record ON bookmark.record_id = record.id
    WHERE bookmark.user_id = %s AND record.deleted_at IS NULL
    UNION
    SELECT likes.user_id, likes.record_id 
    FROM likes
    JOIN record ON likes.record_id = record.id
    WHERE likes.user_id = %s AND record.deleted_at IS NULL
    """
    cursor.execute(sql, (user_id, user_id))
    res = pd.DataFrame(cursor.fetchall(), columns=['user_id', 'record_id'])
    return res
