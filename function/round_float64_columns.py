import pandas as pd
import numpy as np

def round_float64_columns(df, decimal_places=8):
    """
    DataFrame에서 np.float64 타입의 열을 찾아 소숫점 `decimal_places` 자리까지 반올림하는 함수

    Parameters:
    df (pd.DataFrame): 입력 데이터프레임
    decimal_places (int): 반올림할 소수점 자리 수 (기본값 8)

    Returns:
    pd.DataFrame: 변환된 데이터프레임
    """
    # np.float64 타입의 컬럼만 반올림 적용
    float_cols = df.select_dtypes(include=[np.float64]).columns
    df[float_cols] = df[float_cols].round(decimal_places)
    
    return df
