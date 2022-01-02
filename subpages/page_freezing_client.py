# 界面构建
from time import sleep
import streamlit as st
import altair as alt

# 主方法
from database import *


def page_freezing_client():
    st.title('靜止戶資料表') 

    df_table = st.empty()
    df = readForm('freezing_client')
    df_table.write(df)

    st.download_button(
        label="Download data as CSV",
        data=df.to_csv().encode('utf-8'),
        file_name='freezing_client.csv',
        mime='text/csv',

    )

    refresh = st.button("Refresh")
    if refresh:
        df_table.empty()
        df_table.write(df)

    st.sidebar.text('===================================')
    with st.sidebar.expander("查詢資料"):
        st.header('查詢資料')

        discountMax = st.slider('最大折扣', -1, 100, 1)

        ageMin = st.slider('用戶最小年齡', min(df['C_age']), max(df['C_age']), 1)
        ageMax = st.slider('用戶最大年齡', min(df['C_age']), max(df['C_age']), max(df['C_age']))

        tag = st.selectbox('查詢方式',df.columns.values)
        info = st.text_input('內容', '')
        # # Filter dataframe
        if not str(info) == '':
            new_df = df[(df[tag] == info)]
        else:
            new_df = df[(df['C_age'] > ageMin) & (df['C_age'] < ageMax) & (df['C_discount'] <= discountMax)]

        # # write dataframe to screen
    st.header('查詢結果')
    st.write(new_df)
    st.sidebar.text('===================================')
    with st.sidebar.expander("查詢客戶照片"):
        st.header('查詢客戶照片')
        photo_C_ID = st.text_input('照片:客戶ID', '')

        if not str(photo_C_ID) == '':
            photo = list(df[df['C_ID'] == photo_C_ID]['C_photo'])[0]
            print('photo:  ',photo)
            bytes_stream = BytesIO(photo)
            roiimg = Image.open(bytes_stream)

            st.image(roiimg, caption='Cient Head',use_column_width=True)


    st.sidebar.text('===================================')
    with st.sidebar.expander("刪除"):
        st.header('刪除')

        del_ID = st.text_input('刪除ID', '')
        Del_pressed = st.button('刪除資料')
        if Del_pressed:
            print(del_ID)
            print('press!')
            flag_del = delFreezingClient(del_ID)
            if flag_del:
                st.success("Successed")
                df_table.empty()
                df_table.write(df)
            else:
                st.error("Delete failed, please check you parameter or datatype")
    st.sidebar.text('===================================')
    with st.sidebar.expander("统计"):
        st.write('客戶人數')
        st.write(len(df['C_ID']))
        st.text('客戶平均年齡')
        st.write(df['C_age'].sum() / len(df['C_ID']))
    return True