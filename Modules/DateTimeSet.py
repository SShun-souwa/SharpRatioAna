import datetime
import re


# 引数に西暦と月と日を渡してdatetime型に変換して戻す関数。引数の形式によって条件分岐。
def datetime_set(date):
    date = str(date)
    # 正規表現パターンを定義　yyyy*mm*dd yyyy*m*d　等を想定。
    pattern = re.compile(r"(\d{4}).(\d{1,2}).(\d{1,2})")

    # "20220101"のように数字八桁で記述される場合。
    if bool(re.fullmatch(r"\d{8}", date)):
        if date[4] == "0":
            month = date[5]
        else:
            month = date[4:6]
        if date[6] == "0":
            day = date[7]
        else:
            day = date[6:8]
        date = datetime.date(int(date[0:4]), int(month), int(day))
        return date

    # patternで定義したパターンと同じ形式になっている場合。
    if bool(pattern.search(date)):
        pattern = pattern.search(date)
        pattern_set = pattern.groups()
        pattern_set = list(pattern_set)

        # 月、日が0から始まる場合、0を削除
        if len(pattern_set[1]) == 2 and pattern_set[1][0] == "0":
            month = pattern_set[1][1]
            pattern_set[1] = month
        if len(pattern_set[2]) == 2 and pattern_set[2][0] == "0":
            day = pattern_set[2][1]
            pattern_set[2] = day
        date = datetime.date(int(pattern_set[0]), int(pattern_set[1]), int(pattern_set[2]))
        return date

    # 変換の定義がされていない形式が入力されたとき、エラーメッセージを表示して処理を終了する。
    print("the format of inputted date not define。please add format in DateTimeSet")
    exit()


# 引数にデータフレーム、日付の入ったカラムの名前を渡し、対象カラムの日付をdatetime型に変換する
def change_dataframe_day(dataframe, column_name):
    day_list = dataframe[column_name].tolist()
    for i in range(0, len(day_list)):
        day_list[i] = datetime_set(day_list[i])
    dataframe[column_name] = day_list
    return dataframe
