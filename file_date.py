import datetime

# 현재날짜를 가져오고 날짜양식에 맞게 바꾸어준다.
#today = datetime.date.today()
#today_form = str(today.isoformat()).replace('-','')
# ex) today_form = 20240426

# 예) 오늘 날짜를 '20240426' 형태로 반환해준다.
def print_date():
    today = datetime.date.today()
    today_form = str(today.isoformat()).replace('-','')
    return today_form


# 오늘이 몇주차 인지 가져온다.
def print_strftime():
    # 오늘일자
    now_date = datetime.datetime.now()

    # 주차계산 결과값 도출
    return now_date.strftime("%V주차")