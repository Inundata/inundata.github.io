import pandas as pd
import numpy as np

from datetime import datetime
from dateutil.relativedelta import relativedelta

from pathlib import Path
db_function = str(Path.cwd().parent.parent / "function")
file_path = str(Path.cwd().parent.parent / "files")

import sys
sys.path.append(db_function)
sys.path.append(file_path)


from access_db import access_db
from get_cols import get_cols
from round_float64_columns import round_float64_columns


def get_temperature(cur, cols, decimal_function):
    # host = os.getenv("HOST")
    # user = os.getenv("USER")
    # pw = os.getenv("PW")
    # target_db = os.getenv("iMAES_DB")

    # cur, conn = access_db(host, user, pw, target_db)

    # temp table

    target_table = "temperature"

    # cols = get_cols(cur, target_table)

    query = f"""SELECT * FROM {target_table}"""

    cur.execute(query)

    df = pd.DataFrame(cur.fetchall(), columns = cols)
    # df = round_float64_columns(df) # 용량 최소화를 위해 소숫점 8번째 자리까지만 사용
    df = decimal_function(df)

    df_dict = {}

    use_cols = ["cat", "tm", "stnId", "stnNm", "ta", "wc_temp"]
    for stnId in df.stnId.unique():
        df_dict[stnId] = df.loc[df["stnId"] == stnId, use_cols].copy().reset_index(drop = True)

    writer = pd.ExcelWriter(f"{file_path}/temperature_{datetime.today().strftime('%y%m%d')}.xlsx"
                        , engine = "xlsxwriter")

    for stnId in df.stnId.unique():
        df_dict[stnId].to_excel(writer, sheet_name = str(stnId), index = False)

    writer.close()

    # conn.close()

    return print("Temperature table finished")