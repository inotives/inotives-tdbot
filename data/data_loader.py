""" Functions to load data (from API, CSV, database) """
import pathlib
import pandas as pd 
from data.db_conn import DBConnection
from data.data_preprocessing import add_common_tech_indicator

ROOT_DIR = pathlib.Path(__file__).parent.parent.resolve() # Root project directory 
DATA_DIR = f"{ROOT_DIR}/data/files"


def load_csv(csv_filename):
    '''load csv data from the csv folder'''
    df = pd.read_csv(f"{DATA_DIR}/{csv_filename}.csv", parse_dates=True)

    return df 

def load_crypto_ohlcv_from_db(crypto, period=365):
    '''load ohlcv data from database'''
    
    conn = DBConnection()
    conn.create_engine()

    df = conn.read_data_to_df(f"""
    SELECT oc.metric_date , oc.open, oc.high , oc.low , oc."close" , oc.volume 
    FROM ohlcv_cmc oc 
    WHERE oc.crypto = '{crypto}'
        AND oc.metric_date >= CURRENT_DATE - INTERVAL '{period} Days'
    ORDER BY 1 ASC
    ;
    """)
    conn.close()

    data = add_common_tech_indicator(df)
    
    data.set_index('metric_date', inplace=True)

    return data 