import pandas as pd
import math
import statistics
import os
from Modules import DateTimeSet

# 計算結果を出力するディレクトリを確認、無い場合は作成
if not os.path.exists("CalcData"):
    os.mkdir("CalcData")

# 各株価指数のCSVファイルをデータフレーム型で読み込み、株価指数名はkeyとする辞書を作成する

stock_index_list = ["NI225", "TOPIX", "DJI", "SP500", "NASDAQ"]
index_data_dict = {}
for i in stock_index_list:
    data_input = pd.read_csv(filepath_or_buffer="DataSet" + "\\" + i + ".csv",
                             encoding="ms932", sep=",")
    data_input.set_axis(["date", "open", "high", "low", "close", "5MA_value", "25MA_value", "75MA_value",
                         "VWAP", "volume", "5MA_volume", "25MA_volume"], axis="columns", inplace=True)
    index_data_dict[i] = data_input


# 指定した日付の間のデータを抽出し、新たなデータフレームとして戻す

def extract_data(dataframe, days):
    temp_df = dataframe.query(str(days[0]) + "< date < " + str(days[1]))
    temp_df = temp_df.sort_values("date")
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


# クローズプライスのリストからリターンとヒストリカルボラティリティの比を計算し、結果をリスト化して戻す
def calc_return_vi_ratio(close_price_list):
    return_day_list = [0]
    return_vi_ratio_list = []

    for k in range(0, len(close_price_list)):
        if k >= 1:
            # 前日終値とのログリターンを計算し、リスト化
            return_day = math.log(close_price_list[k] / close_price_list[k - 1])
            return_day_list.append(return_day)
        # 算出開始日から3日以降(3日以前は0)のヒストリカルボラティリティを計算し、算出開始日から当日までのリターンから除算し、リスト化
        if k > 2:
            historical_vi = math.sqrt(statistics.stdev(return_day_list[0:k] * 250)) * 100
            return_vi_ratio = (close_price_list[k] / close_price_list[0] * 100 - 100) / historical_vi
            return_vi_ratio_list.append(return_vi_ratio)
        else:
            return_vi_ratio_list.append(0)
    return return_vi_ratio_list


# 計算したい期間のリストを作成
days_list = [[20210110, 20210130], [20210303, 20210425]]
# インデックス毎に上記リストの期間を計算させ、CSVファイルに書き出す
for i in index_data_dict.keys():
    for j in days_list:
        df = extract_data(index_data_dict[i], j)
        close_list = df["close"].tolist()
        df["ReturnViRatio"] = calc_return_vi_ratio(close_list)
        df = DateTimeSet.change_dataframe_day(df,"date")
        df.to_csv("CalcData" + "//" + i + "-" + str(j[0]) + "-" + str(j[1]) + ".csv", index=False, encoding='cp932')
