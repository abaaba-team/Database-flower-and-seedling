# 界面构建
import streamlit as st
import altair as alt

# 主方法
from database import *

def page_fas():
    st.title('花草苗木資料表') 

    df_table = st.empty()
    df = readFromFAS()
    df_table.write(df)
    # st.write(df)
    
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
        FAS_name = st.multiselect('花草名称', df['FAS_name'].unique(), default = df['FAS_name'].unique())
        S_name = st.multiselect('供應商', df['S_name'].unique(), default = df['S_name'].unique())
        Unit = st.multiselect('单位', df['Unit'].unique(), default = df['Unit'].unique())
        StoragePlace = st.multiselect('存放地點', df['StoragePlace'].unique(), default = df['StoragePlace'].unique())


    # Filter dataframe
    new_df = df[(df['FAS_name'].isin(FAS_name)) & (df['Unit'].isin(Unit)) & (df['S_name'].isin(S_name)) & (df['StoragePlace'].isin(StoragePlace))]


    # write dataframe to screen
    st.header('查詢結果')
    st.write(new_df)


    st.sidebar.text('===================================')
    with st.sidebar.expander("新增資料"):
        st.header('新增資料')
        # 參數：名称v 供应商v 总数v 单位/束v 单价v 总价x 储存地址v 购买日期x
        # def addEntityForFAS( name:str, supplier:str, totalCount:float, unit:str, price:float, address:str):
        name = st.text_input('名稱', '')
        supplier = st.text_input('供應商', '')
        totalCount = st.number_input('總數',step = 1)
        unit = st.text_input('單位', '')
        price = st.text_input('單價', '')
        address = st.text_input('地址', '')
        Add_pressed = st.button('新增資料')


        if Add_pressed:
            print(name,supplier,totalCount,unit,price,address)
            print('press!')
            flag_add = addEntityForFAS( name, supplier, int(totalCount), unit, price, address)
            
            if flag_add:
                st.success("Successed")
                df_table.empty()
                df_table.write(df)
            else:
                st.error("addEntity failed, please check you parameter or datatype")


    st.sidebar.text('===================================')
    with st.sidebar.expander("花草小計"):
        st.header('花草小計')
        select_fas = st.multiselect('花草名称', df['FAS_name'].unique())
        count_fas = df[df['FAS_name'].isin(select_fas)]['TotalCount'].sum()
        price_fas = df[df['FAS_name'].isin(select_fas)]['Subtotal'].sum()
        st.write('花草總個數:')
        st.write(count_fas)
        st.write('花草總價:')
        st.write(price_fas)
    st.sidebar.text('===================================')
    with st.sidebar.expander("總和開銷"):
        st.text('總和開銷')
        st.write(df['Subtotal'].sum())
    return True