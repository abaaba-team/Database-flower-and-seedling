# 界面构建
import streamlit as st
import altair as alt

# 主方法
from database import *


def page_supplier():
    st.title('供應商資料表') 

    df_table = st.empty()
    df = readForm('supplier')
    df_table.write(df)

    st.download_button(
        label="Download data as CSV",
        data=df.to_csv().encode('utf-8'),
        file_name='supplier.csv',
        mime='text/csv',

    )

    refresh = st.button("Refresh")
    if refresh:
        df_table.empty()
        df_table.write(df)

    st.sidebar.text('===================================')
    with st.sidebar.expander("查詢資料"):
        st.header('查詢資料')

        tag = st.selectbox('查詢方式',df.columns.values)
        info = st.text_input('內容', '')
        # # Filter dataframe
        new_df = df[(df[tag] == info)]
        # # write dataframe to screen
    st.header('查詢結果')
    st.write(new_df)

    st.sidebar.text('===================================')
    with st.sidebar.expander("新增資料"):
        st.header('新增資料')
        # 參數：FAS_name x P_ID x C_ID v FASID v S_name x TotalPurchase x Price v TotalCount v TotalDiscount x
        # OrderDate v !> EstimateDeliveryDate v ≈ ActualDeliveryDate v R_ID x
        # def addPurchase(C_ID:str, FASID:int, Price:float, TotalCount:int, OrderDate:str, EstimatedDeliveryDate:str, ActualDeliveryDate: str):
        name = st.text_input('名稱', '')
        ID = st.text_input('ID', '')
        phonenumber = st.text_input('手機門號', '')
        mail = st.text_input('郵件', '')
        principle = st.text_input('代理人', '')
        Add_pressed = st.button('新增資料')

        if Add_pressed:
            print(name,ID,phonenumber,mail,principle)
            print('press!')
            flag_add = addSupplier( name, ID, phonenumber, mail, principle)
            if flag_add:
                st.success("Successed")
                df_table.empty()
                df_table.write(df)
            else:
                st.error("add Supplier failed, please check you parameter or datatype")

    st.sidebar.text('===================================')
    with st.sidebar.expander("统计"):
        st.text('供應商個數')
        st.write(len(df['S_ID']))

        st.text('供應商Email重複')
        st.write(df[df['S_mail'].duplicated() == True])

        st.text('供應商代理人重複')
        st.write(df[df['S_principle'].duplicated() == True])
    return True