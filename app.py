from asyncio import new_event_loop
import json
import os
from datetime import date
import streamlit as st

MOOD_MAP = {
    "开心": 2,
    "平静": 1,
    '悲伤': 0,
    '疲惫': -1,
    "焦虑": -2

}
def prepare_chart_data(data):
    """
    准备图表数据

    Args:
        data (list): 心情记录列表

    Returns:
        dict: 包含日期和心情值的字典
    """
    sorted_data = sorted(data, key=lambda x:x["日期"], reverse=True)

    values = []

    for record in sorted_data:
        mood = record["心情"]
        value = MOOD_MAP.get(mood, 0)
        values.append(value)
    return values

def load_data():
    """
    从本地data.json读取数据
    如果文件不存在，则创建一个空数据文件

    Returns:
        list: 心情记录列表
    """

    file_path = "data.json"

    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data 
    

def save_data(data):
    '''
    保存数据到本地data.json文件

    Args:
        data (list): 心情记录列表
    '''

    file_path = "data.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    

def add_mood(data, mood):
    """
    添加新的心情记录(每天只能提交一条)

    Args:
        data (list): 心情记录列表
        mood (str): 用户的心情（happy/sad）
    
    Returns:
        list: 更新后的心情记录列表
    """
    today = date.today().isoformat()
    if any(record["日期"] == today for record in data):
        st.warning("您已提交过相同的心情记录")
        return data

    new_record = {'日期': today, '心情': mood}
    data.append(new_record)

    save_data(data)
    st.success("心情记录添加成功")
    return data

def get_last_7_days(data):
    """
    获取最近7天的心情记录

    Args:
        data (list): 心情记录列表

    Returns:
        list: 最近7天的心情记录列表
    """
    sorted_data = sorted(data, key=lambda x:x["日期"], reverse=True)
    return sorted_data[:7]

def has_submitted_today(data):
    '''
    检查用户是否已提交过相同的心情记录

    Args:
        data (list): 心情记录列表

    Returns:
        bool: 如果用户已提交过相同的心情记录，则返回True，否则返回False
    '''
    today = date.today().isoformat()
    return any(record["日期"] == today for record in data)


def main():
    st.title('心情记录器')
    
    data = load_data()

    mood = st.selectbox("请选择您的心情", ["开心", '平静', "悲伤", '疲惫', '焦虑'])

    submitted = has_submitted_today(data)

    if submitted:
        st.warning("您已提交过相同的心情记录")
    else:
        if st.button('提交'):
            data = add_mood(data, mood)
            st.success("心情记录添加成功")

    st.subheader("最近7天的心情记录")
    last_7_days = get_last_7_days(data)
    for record in last_7_days:
        st.write(f'{record["日期"]} - {record["心情"]}')
    
    st.subheader('最近7天的心情趋势')
    chart_values = prepare_chart_data(last_7_days[::-1])
    st.line_chart(chart_values)


if __name__ == "__main__":
    main()
