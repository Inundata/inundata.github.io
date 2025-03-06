import pandas as pd
from datetime import datetime

from pathlib import Path
db_function = str(Path.cwd().parent.parent / "function")

import sys
sys.path.append(db_function)

from adjust_day_for_temp import adjust_day_based_on_tm_and_hour


def wide_temperature(file_path, temp_fname):

    wide_dict = {}
    stnIds = [108, 159, 143, 133, 156, 112, 114, 119]
    for stnId in stnIds:

        # wide temperature
        temp_long = pd.read_excel(f"{file_path}/{temp_fname}", sheet_name = f"{stnId}")

        temp_long["hour"] = temp_long["tm"].dt.hour

        # wide는 1~24를 사용하므로 이를 위해서 조정
        temp_long = adjust_day_based_on_tm_and_hour(temp_long)
        temp_long.loc[temp_long["hour"] == 0, "hour"] = 24

        # 값 조정
        temp_long["year"], temp_long["month"], temp_long["day"] = temp_long["tm"].dt.year, temp_long["tm"].dt.month, temp_long["tm"].dt.day

        # 첫번째 FOR값은 api의 제공범위로 인해 FOR로 찍히는데, REAL로 갈음하기
        idx = temp_long.loc[temp_long["cat"] == "FOR"].index[0]
        temp_long.at[idx, "cat"] = "REAL"

        # wide로 변환
        temp_wide = pd.pivot_table(temp_long, values = "ta", index = ["cat", "stnId", "year", "month", "day"],  columns="hour")
        temp_wide = temp_wide.reset_index()
        temp_wide = temp_wide.sort_values(by = ["year", "month", "day"])
        temp_wide = temp_wide.reset_index(drop = True)

        # 시작점은 1991년 1월 1일
        temp_wide = temp_wide.loc[(temp_wide["year"] >= 1991) & (temp_wide["month"] >= 1) & (temp_wide["day"] >= 1)]

        # column정보 변경
        temp_wide.rename(columns = {"stnId" : "rc_code"}, inplace = True)
        change_cols = [f"hour{v}" for v in temp_wide.columns[5:]]
        temp_wide.columns =  list(temp_wide.columns[:5]) + change_cols

        wide_dict[stnId] = temp_wide


    writer = pd.ExcelWriter(f"{file_path}/temperature_wide_{datetime.today().strftime('%y%m%d')}.xlsx"
                        , engine = "xlsxwriter")

    for stnId in stnIds:
        wide_dict[stnId].to_excel(writer, sheet_name = f"temp{stnId}p1h", index = False)

    writer.close()
