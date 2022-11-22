import pandas as pd
import math
import statistics

# 各株価指数のCSVファイルをデータフレーム型で読み込み、株価指数名はkeyとする辞書を作成する

stock_index_list = ["NI225", "TOPIX", "DJI", "SP500", "NASDAQ"]
index_data_dict = {}
for i in stock_index_list:
    data_input = pd.read_csv(filepath_or_buffer="DataSet" + "\\" + i + ".csv",
                             encoding="ms932", sep=",")
    data_input.set_axis(["date", "open", "high", "low", "close", "5MA_value", "25MA_value", "75MA_value",
                         "VWAP", "volume", "5MA_volume", "25MA_volume"], axis="columns", inplace=True)
    index_data_dict[i] = data_input


# 指定した日付の間のデータを抽出し、新たなデータフレームとして返す関数

def extract_data(dataframe, days):
    temp_df = dataframe.query(str(days[0]) + "< date < " + str(days[1]))
    temp_df = temp_df.sort_values("date")
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


df = extract_data(index_data_dict["NI225"], [20210110, 20210130])
close_list = df["close"].tolist()

def calc_sharpratio(close_list):
    dayreturn_list = [0]
    sharpratio_list = [0]

    for i in range (0,len(close_list)):
        if (i >= 1) :
            dayreturn = math.log(close_list[i]/close_list[i-1])
            dayreturn_list.append(dayreturn)

    return dayreturn_list


d = calc_sharpratio(close_list)
print(d)

# x = math.e
# x = math.log(x)
# print(x)
