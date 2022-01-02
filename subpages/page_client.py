# 界面构建
from numpy import e
import streamlit as st
import altair as alt

# 主方法
from database import *

def page_client():
    st.title('客戶資料表') 

    df_table = st.empty()
    df = readForm('client')
    df_table.write(df)

    st.download_button(
        label="Download data as CSV",
        data=df.to_csv().encode('utf-8'),
        file_name='fas.csv',
        mime='text/csv',

    )
    refresh = st.button("Refresh")
    if refresh:
        df_table.empty()
        df_table.write(df)

    st.sidebar.text('===================================')
    with st.sidebar.expander("查詢資料"):
        st.header('查詢資料')

        discountMax = st.slider('折扣小于', 1, 100, 100)

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
            try:
                photo = list(df[df['C_ID'] == photo_C_ID]['C_photo'])[0]
                print('photo:  ',photo)
                bytes_stream = BytesIO(photo)
                roiimg = Image.open(bytes_stream)

                st.image(roiimg, caption='Cient Head',use_column_width=True)
            except:
                st.error("Failed, check your input")

    st.sidebar.text('===================================')
    with st.sidebar.expander("编辑客户资料"):
        st.header('编辑客户资料')
        ID_edit = st.text_input('查询:ID', '')
        tag_edit = st.selectbox('编辑:查詢方式',df.columns.values)
        info_edit = st.text_input('编辑:內容', '')
        edit_press = st.button("编辑资料")
        if edit_press:
            flag_edit = editClientWithTag(ID_edit, tag_edit, info_edit)
            if flag_edit:
                st.success("Successed")
                df_table.empty()
                df_table.write(df)
            else:
                st.error("Edit failed, please check you parameter or datatype")


    st.sidebar.text('===================================')
    with st.sidebar.expander("新增資料"):
        st.header('新增資料')
        # 參數：name v, ID v, birthday v, phone v, mail v, age x, photo v, discount="100" v
        # def addClient(name:str, ID, birthday:str, phone, mail:str, photo, discount="100"):  
        name = st.text_input('名稱', '')
        ID = st.text_input('ID', '')
        birthday = st.date_input('生日')
        phone = st.text_input('電話門號', '')
        mail = st.text_input('郵箱', '')


        # photo = st.text_input('地址', '')
        file = open("abaaba.jpg",'rb')
        photo = file.read()
        file.close()

        discount = st.text_input('降價', '100') 
        Add_pressed = st.button('新增資料')

        

        if Add_pressed:
            print(birthday)
            print('press!')
            flag_add = addClient(name, ID, str(birthday), phone, mail, photo, discount)
            if flag_add:
                st.success("Successed")
                df_table.empty()
                df_table.write(df)
            else:
                st.error("addEntity failed, please check you parameter or datatype")

    st.sidebar.text('===================================')
    with st.sidebar.expander("刪除"):
        st.header('刪除')

        del_ID = st.text_input('刪除ID', '')
        Del_pressed = st.button('刪除資料')
        if Del_pressed:
            print(del_ID)
            print('press!')
            flag_del = delClient(del_ID)
            if flag_del:
                st.success("Successed")
                df_table.empty()
                df_table.write(df)
            else:
                st.error("Delete failed, please check you parameter or datatype")
    st.sidebar.text('===================================')
    with st.sidebar.expander("统计"):
        st.text('客戶人數')
        st.write(len(df['C_ID']))
        st.text('客戶平均年齡')
        st.write(df['C_age'].sum() / len(df['C_ID']))
    return True