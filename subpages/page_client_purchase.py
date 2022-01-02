# 界面构建
import streamlit as st
import altair as alt

import datetime

# 主方法
from database import *

def page_client_purchase():
    st.title('客戶購買資料表') 

    df_table = st.empty()
    df = readForm('client_purchase')
    df_table.write(df)

    st.download_button(
        label="Download data as CSV",
        data=df.to_csv().encode('utf-8'),
        file_name='client_purchase.csv',
        mime='text/csv',

    )

    refresh = st.button("Refresh")
    if refresh:
        df_table.empty()
        df_table.write(df)

    st.sidebar.text('===================================')
    with st.sidebar.expander("查詢資料"):
        st.header('查詢資料')
        # 參數：搜索標籤 標籤內容
        # def searchPurchasebyTag(tag:str,info):
        minPurchase = st.slider('最小購買總價', min(df['TotalPurchase']), max(df['TotalPurchase']), 0.01)
        maxPurchase = st.slider('最大購買總價', min(df['TotalPurchase']), max(df['TotalPurchase']), max(df['TotalPurchase']))

        st.write('↑')
        andOrOr = st.checkbox('與√/或x',True)
        st.write('(沒有內容則根據價格範圍查詢)')
        st.write('↓')

        tag = st.selectbox('查詢方式',df.columns.values)
        info = st.text_input('內容', '')
        # # Filter dataframe
        if andOrOr:
            new_df = df[(df[tag] == info) & ((df['TotalPurchase'] > minPurchase) & (df['TotalPurchase'] < maxPurchase))]
        else:
            if str(info) == '':
                new_df = df[(df['TotalPurchase'] > minPurchase) & (df['TotalPurchase'] < maxPurchase)]
            else:
                new_df = df[(df[tag] == info)]

    # # write dataframe to screen
    st.write('查詢結果')
    st.write(new_df)


    st.sidebar.text('===================================')
    with st.sidebar.expander("新增資料"):
        st.header('新增資料')
        # 參數：FAS_name x P_ID x C_ID v FASID v S_name x TotalPurchase x Price v TotalCount v TotalDiscount x
        # OrderDate v !> EstimateDeliveryDate v ≈ ActualDeliveryDate v R_ID x
        # def addPurchase(C_ID:str, FASID:int, Price:float, TotalCount:int, OrderDate:str, EstimatedDeliveryDate:str, ActualDeliveryDate: str):

        C_ID = st.text_input('客戶ID', '')
        FASID = st.text_input('花草ID', '')
        Price = st.text_input('單價', '')
        TotalCount = st.number_input('總數', step=1)

        OrderDate = st.date_input('訂單日期')
        EstimatedDeliveryDate = st.date_input('預計送貨日期')
        hasADD = st.checkbox('已送货',False)
        ActualDeliveryDate = st.date_input('實際送貨日期')
        Add_pressed = st.button('新增資料')

        if Add_pressed:
            
            print(C_ID,FASID,Price,TotalCount,OrderDate,EstimatedDeliveryDate,ActualDeliveryDate)
            print('press!')
            if hasADD:
                flag_add, message = addPurchaseFin(C_ID,int(FASID),Price,int(TotalCount),str(OrderDate),str(EstimatedDeliveryDate),str(ActualDeliveryDate))
                if flag_add:
                    st.success("Successed")
                    df_table.empty()
                    df_table.write(df)
                else:
                    st.error(message)             
            else:
                flag_add, message = addPurchaseBeing(C_ID,int(FASID),Price,int(TotalCount),str(OrderDate),str(EstimatedDeliveryDate))
                if flag_add:
                    st.success("Successed")
                    df_table.empty()
                    df_table.write(df)
                else:
                    st.error(message)

                
    st.sidebar.text('===================================')
    with st.sidebar.expander("新增出貨"):
        st.header('新增出貨')
        ID_edit = st.text_input('貨單ID', '')
        newActualDeliveryDate = st.date_input('出貨日期')
        edit_press = st.button("新增出貨")
        if edit_press:
            flag_edit = editPurchaseDate(ID_edit, newActualDeliveryDate)
            if flag_edit:
                st.success("Successed")
                df_table.empty()
                df_table.write(df)
            else:
                st.error("Edit failed, please check you parameter or datatype")
                


    st.sidebar.text('===================================')
    with st.sidebar.expander("客戶針對某一供應商的購買記錄"):
        st.header('客戶針對某一供應商的購買記錄')
        c_purchase = st.text_input('輸入客戶ID', '')
        s_purchase = st.multiselect('供應商名稱', df['S_name'].unique())

        flag = len(list(df[(df['C_ID'] == c_purchase)]['NotFreezingClient']))
        print('lens: ',flag)
        if flag:

            st.write(df[(df['C_ID'] == c_purchase) & (df['S_name'].isin(s_purchase))])
            st.text('總金額')
            st.text(df[(df['C_ID'] == c_purchase) & (df['S_name'].isin(s_purchase))]['TotalPurchase'].sum())
        else:

            st.write(df[(df['FC_ID'] == c_purchase) & (df['S_name'].isin(s_purchase))])
            st.text('總金額')
            st.text(df[(df['FC_ID'] == c_purchase) & (df['S_name'].isin(s_purchase))]['TotalPurchase'].sum())
        

        


    st.sidebar.text('===================================')
    with st.sidebar.expander("全體客戶針對某一供應商的購買記錄"):
        st.header('全體客戶針對某一供應商的購買記錄')
        s_total_purchase = st.multiselect('供應商', df['S_name'].unique())


        st.write(df[df['S_name'].isin(s_total_purchase)])
        st.text('總金額')
        st.text(df[df['S_name'].isin(s_total_purchase)]['TotalPurchase'].sum())

    st.sidebar.text('===================================')
    with st.sidebar.expander("客戶購買總金額"):
        st.header('客戶購買總金額')
        c_total_purchase = st.text_input('請輸入客戶ID', '')

        # st.write(df[(df['C_ID'] == c_total_purchase)])
        # st.text('總金額')
        # st.text(df[(df['C_ID'] == c_total_purchase)]['TotalPurchase'].sum())
        flag = len(list(df[(df['C_ID'] == c_total_purchase)]['NotFreezingClient']))
        print('lens: ',flag)
        if flag:
            st.write(df[(df['C_ID'] == c_total_purchase)])
            st.text('總金額')
            st.text(df[(df['C_ID'] == c_total_purchase)]['TotalPurchase'].sum())
        else:
            st.write(df[(df['FC_ID'] == c_total_purchase)])
            st.text('總金額')
            st.text(df[(df['FC_ID'] == c_total_purchase)]['TotalPurchase'].sum())
            

    st.sidebar.text('===================================')
    with st.sidebar.expander("全體客戶購買總金額"):
        st.header('全體客戶購買總金額')
        st.text(df['TotalPurchase'].sum())

    st.sidebar.text('===================================')
    with st.sidebar.expander("客戶購買排序"):
        st.header('客戶購買排序')

        freezing_client_info_df = pd.DataFrame(readForm('freezing_client'))
        client_info_df = pd.DataFrame(readForm('client'))


        client_df = pd.DataFrame(columns=('C_ID','C_name','C_mail','C_phone','TotalPurchase'))


        # .dropna(how='all')#删除所有内容均为缺失值的行
        tmp_df = pd.DataFrame(df['C_ID'].unique()).dropna(how='all')[0]
        for i in tmp_df:
            tmp_c = client_info_df[client_info_df['C_ID'] == i]
            # print('tmp_c',str(tmp_c['C_name']).split()[1])
            new_row = pd.DataFrame({'C_ID':[i],'C_name':str(tmp_c['C_name']).split()[1],'C_mail':str(tmp_c['C_mail']).split()[1],'C_phone':str(tmp_c['C_phonenumber']).split()[1],'TotalPurchase':[df[df['C_ID'] == i]['TotalPurchase'].sum()]})
            # print(new_row)
            client_df = client_df.append(new_row,  ignore_index=True)

        tmp_df = pd.DataFrame(df['FC_ID'].unique()).dropna(how='all')[0]
        for i in tmp_df:
            tmp_c = freezing_client_info_df[freezing_client_info_df['C_ID'] == i]
            new_row = pd.DataFrame({'C_ID':[i],'C_name':str(tmp_c['C_name']).split()[1],'C_mail':str(tmp_c['C_mail']).split()[1],'C_phone':str(tmp_c['C_phonenumber']).split()[1],'TotalPurchase':[df[df['FC_ID'] == i]['TotalPurchase'].sum()]})
            # print(new_row)
            client_df = client_df.append(new_row,  ignore_index=True)
        
        # print(client_df)
        st.write(client_df)

    st.sidebar.text('===================================')
    with st.sidebar.expander("尚未出貨"):
        st.header('尚未出貨')
        fas_wait = df[df['ActualDeliveryDate'].isna()]
        st.write(fas_wait)

    return True