import pandas as pd
from dateutil.relativedelta import relativedelta

def adjust_day_based_on_tm_and_hour(df):
    # 조건: hour가 0인 경우만 적용
    mask = df["hour"] == 0
    
    # 'day' 컬럼 업데이트 (조건에 맞는 행만 변경)
    df.loc[mask, "tm"] = (df.loc[mask, "tm"].apply(lambda x: x - relativedelta(hours = 1)))

    return df
