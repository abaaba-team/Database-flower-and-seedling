import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import time #正规时间

import re #正则match

from PIL import Image

from io import BytesIO


# 初始化数据库连接
USER = 'root'
PASSWORD = 'abc'
ADDRESS = 'jp-tyo-ilj-1.natfrp.cloud'
PORT = '49930'
DB = 'fas'
CHARSET = 'utf-8'
engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, ADDRESS, PORT, DB),encoding = 'utf-8')
# =========================================
# 功能：：花草种类：：搜索
# 參數：搜尋標籤 標籤內容
def searchFASKindbyTag(tag:str, info):
    info = str(info)
    try:
        sql_query = 'select * from flower_and_seedling where '+tag+' = "'+info+'";'
        df_read = pd.read_sql_query(sql_query, engine)
    except:
        print("Type of info is Invalid!!")
    return df_read
# =========================================
# 功能：：花草种类：：添加
# 參數：名称v
def addEntityForFASKind( name:str):
#     依據參數上傳data
    df_write = pd.DataFrame({'FAS_name': [name]})
    # df_write.to_sql('flower_and_seedling', engine, if_exists="append" ,index=False)
    try:
        df_write.to_sql('flower_and_seedling', engine, if_exists="append" ,index=False)
        return True
    except:
        print("addEntity failed, please check you parameter or datatype")
        return False
# =========================================
# 功能：：花草苗木資料表：：讀取表格
# 參數: <empty>
def readFromFAS():
    sql_query = 'select * from supplier_relationship_with_flower;'
    df_read = pd.read_sql_query(sql_query, engine)
    for i in range(len(df_read['FASID'])):
        l = str(df_read['FASID'][i]).zfill(10)
        df_read['FASID'][i] = l[:2]+'-'+l[2:5]+'-'+l[5:9]+'-'+l.zfill(10)[-1]
    return df_read
# =========================================
# 功能：：花草苗木：：新增资料
# 參數：名称v 供应商v 总数v 单位/束v 单价v 总价x 储存地址v 购买日期x
def addEntityForFAS( name:str, supplier:str, totalCount:float, unit:str, price:float, address:str):
#     依據供應商查看表格
    supplierData = searchSupplierbyTag('S_name',supplier)
#     供應商不存在報錯
    if len(supplierData) == 0:
        print("Supplier not exist, please addSupplier first!!")
        return False
    faskind = searchFASKindbyTag('FAS_name',name)
    if len(faskind) == 0:
        addEntityForFASKind(name)
    fid = searchFASKindbyTag('FAS_name',name)['F_ID'][0]
#     依據參數上傳data
    df_write = pd.DataFrame({'F_ID':[fid], 'FAS_name': [name], 'S_name': [supplier], 'TotalCount': [totalCount],'Unit':[unit],'Price':[price],'Subtotal':[totalCount * price],'StoragePlace':[address],'PurchaseDate':[time.strftime("%Y-%m-%d", time.localtime())]})
    try:
        df_write.to_sql('supplier_relationship_with_flower', engine, if_exists="append" ,index=False)
        return True
    except:
        print("addEntity failed, please check you parameter or datatype")
        return False
# =========================================
# 辅助功能：判断字串是否是数字构成的
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    import unicodedata
    try:
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    if len(s) < 2:
        return False
    try:
        d = 0
        if s.startswith('－'):
            s = s[1:]
        for c in s:
            if c == '－': # 全角减号
                return False
                
            if c == '．': # 全角点号
                if d > 0:
                    return False
                else:
                    d = 1
                    continue
            unicodedata.numeric(c)
        return True
    except (TypeError, ValueError):
        pass
    return False
# =========================================
# 功能：：花草苗木：：查询资料
# 參數：搜尋標籤 標籤內容
def searchFASbyTag(tag:str, info):
    info = str(info)
    try:
        sql_query = 'select * from supplier_relationship_with_flower where '+tag+' = "'+info+'";'
        df_read = pd.read_sql_query(sql_query, engine)
    except:
        print("Type of info is Invalid!!")
    return df_read
# =========================================
# 功能：：全局（花草苗木）：：列印查询结果资料
# 參數：表格
def showData(data):
    try:
        print(data)
        return True
    except:
        print("Invalid..")
        return False
# =========================================
# 輔助功能：判断是否是一个有效的日期字符串
def is_valid_date(str):
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except:
        return False
# 輔助功能：查看資料是否合法
def checkClientDataValid(name:str, ID, birthday:str, phone, mail:str, photo, discount):
#     ID不符合
    if not(re.match('[a-zA-Z]{1}[0-9]{9}',ID) or re.match('[0-9]{8}',ID)):
        print("Invalid ID! 需要一位英文字母加九位數字 或者 八碼數字字串")
        return False
#     日期不符合
    if not is_valid_date(birthday):
        print("Invalid Date! 日期格式需要%Y-%m-%d")
        return False
#     郵箱不符合
    if not re.match('([a-zA-Z0-9]+)@([a-z]+)\.com',mail):
        print("Invalid email!")
        return False
#     折扣格式不符合
    if not re.match('[0-9]{3}',discount):
        print("Invalid discount! 請輸入三位實數")
        return False
#     折扣範圍不符合
    if int(discount) > 100 or int(discount) < 0:
        print("Discount must between 0,100!!")
        return False
    return True
# =========================================
# 功能：：凍結客戶資料表：：查詢客戶
# 參數：搜索標籤 標籤內容
def searchFreezingClientbyTag(tag:str, info):
    try:
        if(isinstance(info,int)):
            sql_query = 'select * from freezing_client where '+tag+' = '+str(info)+';'
            df_read = pd.read_sql_query(sql_query, engine)
        elif(isinstance(info,str)):
            sql_query = 'select * from freezing_client where '+tag+' = "'+info+'";'
            df_read = pd.read_sql_query(sql_query, engine)
    except:
        print("Type of info is Invalid!!")
        return False
    return df_read
# =========================================
# 功能：：客戶資料表（凍結客戶資料表）：：轉移資料（刪除資料）
# 參數：客戶/凍結客戶id
def delFreezingClient(C_id):
    if re.match('[0-9]{8}',C_id):
        C_id = 'C3'+C_id
#     查找當前資料表
    data = searchFreezingClientbyTag('C_ID',C_id)
    C_id = str(C_id)
#     如果資料不存在，報錯
    if len(data) == 0:
        print("No data can be deleted!!")
        return False
#     獲取purchase的記錄
    sql_query = 'select P_ID from client_purchase where FC_ID = "{}";'.format(C_id)
    P_IDList = pd.read_sql_query(sql_query, engine)
#     準備刪除步驟
    sql_query = 'delete from freezing_client where C_ID = "'+C_id+'";'
    try:
#         為客戶資料表添加資料
        data.to_sql('client', engine, if_exists="append" ,index=False)
#         執行刪除
        pd.read_sql_query(sql_query, engine)
    except:
        print("",end="")
#     依據PID查找需要更改flag狀態的purchase
    for i in P_IDList["P_ID"]:
        try:
            sql_query = 'update client_purchase set NotFreezingClient = "1",C_ID = "{}" where P_ID = {};'.format(C_id,i)
            pd.read_sql_query(sql_query, engine)
        except:
            print("",end="")
    return True
# =========================================
# 功能：：凍結客戶資料表：：編輯
# 參數：凍結客戶id 修改目標標籤 標籤內容
def editFreezingClientWithTag(ID:str, tag:str, info):
    if re.match('[0-9]{8}',ID):
        ID = 'C3'+ID
    data = searchFreezingClientbyTag('C_ID',ID)
#     print(data)
    if len(data)==0:
        print('Data not exist!!')
        return False
    sql_query = 'update freezing_client set {} = "{}" where C_ID = "{}";'.format(tag, info, ID)
#     pd.read_sql_query(sql_query, engine)
    try:
        pd.read_sql_query(sql_query, engine)
    except:
        print("",end="")
    return True
# =========================================
# 功能：：客户资料表：：新增资料
# 參數：name v, ID v, birthday v, phone v, mail v, age x, photo v, discount="100" v
def addClient(name:str, ID, birthday:str, phone, mail:str, photo, discount="100"):
    ID = str(ID)
    phone = str(phone)
    discount = str(discount).zfill(3)
#     如果格式不符合退出
    if not checkClientDataValid(name, ID, birthday, phone, mail, photo, discount):
        return False
#     修改ID格式
    if re.match('[0-9]{8}',ID):
        ID = 'C3'+ID
#     如果凍結資料表中存在該客戶 刪除凍結資料表的資料，移動到客戶資料 返回True
    if not len(searchFreezingClientbyTag('C_ID',ID)) == 0: 
        delFreezingClient(ID)
        return True
#     修改生日格式
    birthday = time.strptime(birthday, "%Y-%m-%d")
#     計算年齡
    age = int(time.asctime(time.localtime(time.time()))[-4:]) - int(time.asctime(birthday)[-4:])
#     準備寫入資料
    df_write = pd.DataFrame({'C_name': [name], 'C_ID': [ID], 'C_birthday': [birthday],'C_phonenumber':[phone],'C_mail':[mail],'C_age':[age],'C_photo':[photo],'C_discount':[discount]})
    try:
#         寫入資料
        df_write.to_sql('client', engine, if_exists="append" ,index=False)
        return True
    except:
        print("addEntity failed, please check you parameter or datatype")
        return False
# =========================================
# 功能：：客戶資料表：：查詢客戶
# 參數： 搜索標籤 標籤內容
def searchClientbyTag(tag:str, info):
    try:
        if(isinstance(info,int)):
            sql_query = 'select * from client where '+tag+' = '+str(info)+';'
            df_read = pd.read_sql_query(sql_query, engine)
        elif(isinstance(info,str)):
            sql_query = 'select * from client where '+tag+' = "'+info+'";'
            df_read = pd.read_sql_query(sql_query, engine)
    except:
        print("Type of info is Invalid!!")
        return False
    return df_read
# =========================================
# 功能：：客戶資料表：：刪除資料
# 參數：客戶id
def delClient(C_id):
    C_id = str(C_id)
#     修改ID格式
    if re.match('[0-9]{8}',C_id):
        C_id = 'C3'+C_id
#     查找客戶資料
    data = searchClientbyTag('C_ID',C_id)
#     資料不存在報錯
    if len(data) == 0:
        print("No data can be deleted!!")
        return False
#     獲取該id相關purchase
    sql_query = 'select P_ID from client_purchase where C_ID = "{}";'.format(C_id)
    P_IDList = pd.read_sql_query(sql_query, engine)
#     準備刪除資料
    sql_query = 'delete from client where C_ID = "'+C_id+'";'
#     準備轉存的資料
    try:
#         給凍結客戶資料表添加資料
        data.to_sql('freezing_client', engine, if_exists="append" ,index=False)
        pd.read_sql_query(sql_query, engine)
    except:
        print("",end="")
#     轉移purchase內客戶id狀態
    for i in P_IDList["P_ID"]:
        try:
            sql_query = 'update client_purchase set NotFreezingClient = "0",FC_ID = "{}" where P_ID = {};'.format(C_id,i)
            pd.read_sql_query(sql_query, engine)
        except:
            print("",end="")
    return True
# =========================================
# 功能：：凍結客戶資料表：：編輯
# 參數：客戶id 修改客戶標籤 標籤內容
def editClientWithTag(ID:str, tag:str, info):
    if re.match('[0-9]{8}',ID):
        ID = 'C3'+ID
    data = searchClientbyTag('C_ID',ID)
    if len(data)==0:
        print('Data not exist!!')
        return False
    sql_query = 'update client set {} = "{}" where C_ID = "{}";'.format(tag, info, ID)
#     pd.read_sql_query(sql_query, engine)
    try:
        pd.read_sql_query(sql_query, engine)
    except:
        print("",end="")
    return True
# =========================================
# 功能：：供應商資料表：：新增
# 參數：name ID phonenumber mail principle
def addSupplier(name:str, ID:str, phonenumber:int, mail:str, principle:str):
#     判斷id是否合法
    if not(re.match('[a-zA-Z]{1}[0-9]{9}',ID) or re.match('[0-9]{8}',ID)):
        print("Invalid ID! 需要一位英文字母加九位數字 或者 八碼數字字串")
        return False
#     判斷郵箱是否合法
    if not re.match('([a-zA-Z0-9]+)@([a-z]+)\.com',mail):
        print("Invalid email!")
        return False
#     格式化id
    if re.match('[0-9]{8}',ID):
        ID = 'C3'+ID
#     獲取供應商信息
    data = searchSupplierbyTag('S_ID',ID)
#     供應商存在報錯，結束
    if not len(data) == 0:
        print("Supplier Already Exist!!")
        return False
#     準備寫入資料
    df_write = pd.DataFrame({'S_name': [name],'S_ID':[ID],'S_phonenumber':[phonenumber],'S_mail':[mail],'S_principle':[principle]})
    try:
#         寫入資料
        df_write.to_sql('supplier', engine, if_exists="append" ,index=False)
        return True
    except:
        print("addEntity failed, please check you parameter or datatype")
        return False
# =========================================
# 功能：：供應商資料表：：查詢供應商
# 參數：搜索標籤 標籤內容
def searchSupplierbyTag(tag:str, info):
#     格式化id
    if tag == 'S_ID' and re.match('[0-9]{8}',info):
        info = 'C3'+info
#     查找
    try:
        if(isinstance(info,int)):
            sql_query = 'select * from supplier where '+tag+' = '+str(info)+';'
            df_read = pd.read_sql_query(sql_query, engine)
        elif(isinstance(info,str)):
            sql_query = 'select * from supplier where '+tag+' = "'+info+'";'
            df_read = pd.read_sql_query(sql_query, engine)
    except:
        print("Type of info is Invalid!!")
        return False
    return df_read
# =========================================
# 功能：：客戶購買資料表：：新增
# 參數：FAS_name x P_ID x C_ID v FASID v S_name x TotalPurchase x Price v TotalCount v TotalDiscount x
# OrderDate v !> EstimateDeliveryDate v ≈ ActualDeliveryDate v R_ID x
def addPurchase(C_ID:str, FASID:int, Price:float, TotalCount:int, OrderDate:str, EstimatedDeliveryDate:str, ActualDeliveryDate: str):
#     判斷id是否合法
    if not(re.match('[a-zA-Z]{1}[0-9]{9}',C_ID) or re.match('[0-9]{8}',C_ID)):
        print("Invalid ID! 需要一位英文字母加九位數字 或者 八碼數字字串")
        return False
#     判斷日期是否符合格式
    if not (is_valid_date(OrderDate) and is_valid_date(EstimatedDeliveryDate) and is_valid_date(ActualDeliveryDate)):
        print("Invalid Date! 日期格式需要%Y-%m-%d")
        return False
#     確認訂購日期與預計交貨日期和實際交貨日期關係
    deltaTimeOrderEstimated = time.mktime(time.strptime(OrderDate,"%Y-%m-%d")) - time.mktime(time.strptime(EstimatedDeliveryDate,"%Y-%m-%d"))
    deltaTimeOrderActual = time.mktime(time.strptime(OrderDate,"%Y-%m-%d")) - time.mktime(time.strptime(ActualDeliveryDate,"%Y-%m-%d"))
    if deltaTimeOrderEstimated > 0 or deltaTimeOrderActual > 0:
        print("「訂購日期」必須在「預計交貨日期」與「實際交貨日期」之前或同一天!!")
        return False
#     格式化id
    if re.match('[0-9]{8}',C_ID):
        C_ID = 'C3'+C_ID
#     獲取花草苗木資料表
    FASData = searchFASbyTag('FASID',FASID)
#     獲取客戶資料表
    ClientData = searchClientbyTag('C_ID',C_ID)
#     獲取歷史交易
    PurchaseData = searchPurchasebyTag('FASID',FASID)
#     資料不存在報錯，退出
    if len(FASData) == 0 or len(ClientData) == 0:
        print("Data not exist!!")
        return False
#     計算交易消耗商品總數
    count = 0
#     print(PurchaseData['TotalCount'])
    for i in PurchaseData['TotalCount']:
        count = count + i
    if count + TotalCount > FASData['TotalCount'][0]:
        print("商品不足，請更改購買數目！當前id:{} ,總數{}".format(C_ID,FASData['TotalCount'] - count))
        return False
#     準備寫入資料                                                                                            
    df_write = pd.DataFrame({'NotFreezingClient':1,'FAS_name': [FASData['FAS_name'][0]],'C_ID':[C_ID],'FASID':[FASID],'S_name':[FASData['S_name'][0]],'TotalPurchase':[Price * TotalCount],'Price':[Price],'TotalCount':[TotalCount],'TotalDiscount':[float(Price * TotalCount)*float(int(ClientData['C_discount'][0])/100)],'OrderDate':OrderDate,'EstimatedDeliveryDate':EstimatedDeliveryDate,'ActualDeliveryDate':ActualDeliveryDate})
    try:
        df_write.to_sql('client_purchase', engine, if_exists="append" ,index=False)
        return True
    except:
        print("addEntity failed, please check you parameter or datatype")
        return False
# =========================================
# 功能：：客戶購買資料表：：搜索
# 參數：搜索標籤 標籤內容
def searchPurchasebyTag(tag:str,info):
    if tag == 'C_ID' and re.match('[0-9]{8}',info):
        info = 'C3'+info
    try:
        if(isinstance(info,int)):
            sql_query = 'select * from client_purchase where '+tag+' = '+str(info)+';'
            df_read = pd.read_sql_query(sql_query, engine)
        elif(isinstance(info,str)):
            sql_query = 'select * from client_purchase where '+tag+' = "'+info+'";'
            df_read = pd.read_sql_query(sql_query, engine)
    except:
        print("Type of info is Invalid!!")
        return False
    return df_read
# =========================================
def readForm(name:str):
    sql_query = 'select * from '+name+';'
    df_read = pd.read_sql_query(sql_query, engine)
    return df_read

#========================================================================================================================================





















st.sidebar.title("蒙德花園") #sidebar 標題

Database_table = st.sidebar.selectbox( #資料庫選擇
    "資料庫",
    ("花草苗木資料表", "客戶資料表", "靜止戶資料表","供應商資料表","客戶購買資料表")
)



if Database_table=="花草苗木資料表":
    st.title('花草苗木資料表') 


    df = readFromFAS()
    st.write(df)


    st.sidebar.text('查詢資料')
    FAS_name = st.sidebar.multiselect('花草名称', df['FAS_name'].unique(), default = df['FAS_name'].unique())
    S_name = st.sidebar.multiselect('供應商', df['S_name'].unique(), default = df['S_name'].unique())
    Unit = st.sidebar.multiselect('单位', df['Unit'].unique(), default = df['Unit'].unique())
    StoragePlace = st.sidebar.multiselect('存放地點', df['StoragePlace'].unique(), default = df['StoragePlace'].unique())


    # Filter dataframe
    new_df = df[(df['FAS_name'].isin(FAS_name)) & (df['Unit'].isin(Unit)) & (df['S_name'].isin(S_name)) & (df['StoragePlace'].isin(StoragePlace))]


    # write dataframe to screen
    st.write('查詢結果')
    st.write(new_df)

    st.sidebar.text('===================================')
    st.sidebar.text('新增資料')
    # 參數：名称v 供应商v 总数v 单位/束v 单价v 总价x 储存地址v 购买日期x
    # def addEntityForFAS( name:str, supplier:str, totalCount:float, unit:str, price:float, address:str):
    name = st.sidebar.text_input('名稱', '')
    supplier = st.sidebar.text_input('供應商', '')
    totalCount = st.sidebar.number_input('總數',step = 1)
    unit = st.sidebar.text_input('單位', '')
    price = st.sidebar.text_input('單價', '')
    address = st.sidebar.text_input('地址', '')
    Add_pressed = st.sidebar.button('新增資料')


    if Add_pressed:
        print(name,supplier,totalCount,unit,price,address)
        print('press!')
        addEntityForFAS( name, supplier, int(totalCount), unit, price, address)


    st.sidebar.text('===================================')
    st.sidebar.text('花草小計')
    select_fas = st.sidebar.multiselect('花草名称', df['FAS_name'].unique())
    count_fas = df[df['FAS_name'].isin(select_fas)]['TotalCount'].sum()
    price_fas = df[df['FAS_name'].isin(select_fas)]['Subtotal'].sum()
    st.sidebar.write('花草總個數:')
    st.sidebar.write(count_fas)
    st.sidebar.write('花草總價:')
    st.sidebar.write(price_fas)
    st.sidebar.text('===================================')
    st.sidebar.text('總和開銷')
    st.sidebar.write(df['Subtotal'].sum())












if Database_table=="客戶資料表":
    st.title('客戶資料表') 


    df = readForm('client')
    st.write(df)


    st.sidebar.text('查詢資料')

    discountMax = st.sidebar.slider('最大折扣', -1, 100, 1)

    ageMin = st.sidebar.slider('用戶最小年齡', min(df['C_age']), max(df['C_age']), 1)
    ageMax = st.sidebar.slider('用戶最大年齡', min(df['C_age']), max(df['C_age']), 1)

    tag = st.sidebar.selectbox('查詢方式',df.columns.values)
    info = st.sidebar.text_input('內容', '')
    # # Filter dataframe
    if not str(info) == '':
        new_df = df[(df[tag] == info)]
    else:
        new_df = df[(df['C_age'] > ageMin) & (df['C_age'] < ageMax) & (df['C_discount'] <= discountMax)]


    # # write dataframe to screen
    st.write('查詢結果')
    st.write(new_df)

    st.sidebar.text('===================================')
    st.sidebar.text('查詢客戶照片')
    photo_C_ID = st.sidebar.text_input('照片:客戶ID', '')

    if not str(photo_C_ID) == '':
        photo = list(df[df['C_ID'] == photo_C_ID]['C_photo'])[0]
        print('photo:  ',photo)
        bytes_stream = BytesIO(photo)
        roiimg = Image.open(bytes_stream)

        st.sidebar.image(roiimg, caption='Cient Head',use_column_width=True)


    st.sidebar.text('===================================')
    st.sidebar.text('新增資料')
    # 參數：name v, ID v, birthday v, phone v, mail v, age x, photo v, discount="100" v
    # def addClient(name:str, ID, birthday:str, phone, mail:str, photo, discount="100"):  
    name = st.sidebar.text_input('名稱', '')
    ID = st.sidebar.text_input('ID', '')
    birthday = st.sidebar.date_input('生日')
    phone = st.sidebar.text_input('電話門號', '')
    mail = st.sidebar.text_input('郵箱', '')


    # photo = st.sidebar.text_input('地址', '')
    file = open("abaaba.jpg",'rb')
    photo = file.read()
    file.close()

    discount = st.sidebar.text_input('降價', '100') 
    Add_pressed = st.sidebar.button('新增資料')

    

    if Add_pressed:
        print(birthday)
        print('press!')
        addClient(name, ID, str(birthday), phone, mail, photo, discount)

    st.sidebar.text('===================================')
    st.sidebar.text('刪除')

    del_ID = st.sidebar.text_input('刪除ID', '')
    Del_pressed = st.sidebar.button('刪除資料')
    if Del_pressed:
        print(del_ID)
        print('press!')
        delClient(del_ID)
    st.sidebar.text('===================================')
    st.sidebar.text('客戶人數')
    st.sidebar.write(len(df['C_ID']))
    st.sidebar.text('客戶平均年齡')
    st.sidebar.write(df['C_age'].sum() / len(df['C_ID']))










if Database_table=="靜止戶資料表":
    st.title('靜止戶資料表') 


    df = readForm('freezing_client')
    st.write(df)


    st.sidebar.text('查詢資料')

    discountMax = st.sidebar.slider('最大折扣', -1, 100, 1)

    ageMin = st.sidebar.slider('用戶最小年齡', min(df['C_age']), max(df['C_age']), 1)
    ageMax = st.sidebar.slider('用戶最大年齡', min(df['C_age']), max(df['C_age']), 1)

    tag = st.sidebar.selectbox('查詢方式',df.columns.values)
    info = st.sidebar.text_input('內容', '')
    # # Filter dataframe
    if not str(info) == '':
        new_df = df[(df[tag] == info)]
    else:
        new_df = df[(df['C_age'] > ageMin) & (df['C_age'] < ageMax) & (df['C_discount'] <= discountMax)]

    # # write dataframe to screen
    st.write('查詢結果')
    st.write(new_df)
    st.sidebar.text('===================================')
    st.sidebar.text('查詢客戶照片')
    photo_C_ID = st.sidebar.text_input('照片:客戶ID', '')

    if not str(photo_C_ID) == '':
        photo = list(df[df['C_ID'] == photo_C_ID]['C_photo'])[0]
        print('photo:  ',photo)
        bytes_stream = BytesIO(photo)
        roiimg = Image.open(bytes_stream)

        st.sidebar.image(roiimg, caption='Cient Head',use_column_width=True)


    st.sidebar.text('===================================')
    st.sidebar.text('刪除')

    del_ID = st.sidebar.text_input('刪除ID', '')
    Del_pressed = st.sidebar.button('刪除資料')
    if Del_pressed:
        print(del_ID)
        print('press!')
        delFreezingClient(del_ID)
    st.sidebar.text('===================================')
    st.sidebar.text('客戶人數')
    st.sidebar.write(len(df['C_ID']))
    st.sidebar.text('客戶平均年齡')
    st.sidebar.write(df['C_age'].sum() / len(df['C_ID']))










if Database_table=="供應商資料表":
    st.title('供應商資料表') 


    df = readForm('supplier')
    st.write(df)

    
    st.sidebar.text('查詢資料')

    tag = st.sidebar.selectbox('查詢方式',df.columns.values)
    info = st.sidebar.text_input('內容', '')
    # # Filter dataframe
    new_df = df[(df[tag] == info)]
    # # write dataframe to screen
    st.write('查詢結果')
    st.write(new_df)

    st.sidebar.text('===================================')
    st.sidebar.text('新增資料')
    # 參數：FAS_name x P_ID x C_ID v FASID v S_name x TotalPurchase x Price v TotalCount v TotalDiscount x
    # OrderDate v !> EstimateDeliveryDate v ≈ ActualDeliveryDate v R_ID x
    # def addPurchase(C_ID:str, FASID:int, Price:float, TotalCount:int, OrderDate:str, EstimatedDeliveryDate:str, ActualDeliveryDate: str):
    name = st.sidebar.text_input('名稱', '')
    ID = st.sidebar.text_input('ID', '')
    phonenumber = st.sidebar.text_input('手機門號', '')
    mail = st.sidebar.text_input('郵件', '')
    principle = st.sidebar.text_input('代理人', '')
    Add_pressed = st.sidebar.button('新增資料')

    if Add_pressed:
        print(name,ID,phonenumber,mail,principle)
        print('press!')
        addSupplier( name, ID, phonenumber, mail, principle)

    st.sidebar.text('===================================')
    st.sidebar.text('供應商個數')
    st.sidebar.write(len(df['S_ID']))

    st.sidebar.text('供應商Email重複')
    st.sidebar.write(df[df['S_mail'].duplicated() == True])

    st.sidebar.text('供應商代理人重複')
    st.sidebar.write(df[df['S_principle'].duplicated() == True])











if Database_table=="客戶購買資料表":
    st.title('客戶購買資料表') 


    df = readForm('client_purchase')
    st.write(df)

    
    st.sidebar.text('查詢資料')
    # 參數：搜索標籤 標籤內容
    # def searchPurchasebyTag(tag:str,info):
    minPurchase = st.sidebar.slider('最小購買總價', min(df['TotalPurchase']), max(df['TotalPurchase']), 0.01)
    maxPurchase = st.sidebar.slider('最大購買總價', min(df['TotalPurchase']), max(df['TotalPurchase']), 0.01)

    st.sidebar.write('↑')
    andOrOr = st.sidebar.checkbox('與√/或x',True)
    st.sidebar.write('(沒有內容則根據價格範圍查詢)')
    st.sidebar.write('↓')

    tag = st.sidebar.selectbox('查詢方式',df.columns.values)
    info = st.sidebar.text_input('內容', '')
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
    st.sidebar.text('新增資料')
    # 參數：FAS_name x P_ID x C_ID v FASID v S_name x TotalPurchase x Price v TotalCount v TotalDiscount x
    # OrderDate v !> EstimateDeliveryDate v ≈ ActualDeliveryDate v R_ID x
    # def addPurchase(C_ID:str, FASID:int, Price:float, TotalCount:int, OrderDate:str, EstimatedDeliveryDate:str, ActualDeliveryDate: str):

    C_ID = st.sidebar.text_input('客戶ID', '')
    FASID = st.sidebar.text_input('花草ID', '')
    Price = st.sidebar.text_input('單價', '')
    TotalCount = st.sidebar.number_input('總數', step=1)

    OrderDate = st.sidebar.date_input('訂單日期')
    EstimatedDeliveryDate = st.sidebar.date_input('預計送貨日期')
    ActualDeliveryDate = st.sidebar.date_input('實際送貨日期')
    Add_pressed = st.sidebar.button('新增資料')

    if Add_pressed:
        print(C_ID,FASID,Price,TotalCount,OrderDate,EstimatedDeliveryDate,ActualDeliveryDate)
        print('press!')
        addPurchase(C_ID,int(FASID),Price,int(TotalCount),str(OrderDate),str(EstimatedDeliveryDate),str(ActualDeliveryDate))

    st.sidebar.text('===================================')
    st.sidebar.text('客戶針對某一供應商的購買記錄')
    c_purchase = st.sidebar.text_input('輸入客戶ID', '')
    s_purchase = st.sidebar.multiselect('供應商名稱', df['S_name'].unique())

    flag = len(list(df[(df['C_ID'] == c_purchase)]['NotFreezingClient']))
    print('lens: ',flag)
    if flag:

        st.sidebar.write(df[(df['C_ID'] == c_purchase) & (df['S_name'].isin(s_purchase))])
        st.sidebar.text('總金額')
        st.sidebar.text(df[(df['C_ID'] == c_purchase) & (df['S_name'].isin(s_purchase))]['TotalPurchase'].sum())
    else:

        st.sidebar.write(df[(df['FC_ID'] == c_purchase) & (df['S_name'].isin(s_purchase))])
        st.sidebar.text('總金額')
        st.sidebar.text(df[(df['FC_ID'] == c_purchase) & (df['S_name'].isin(s_purchase))]['TotalPurchase'].sum())
    

    


    st.sidebar.text('===================================')
    st.sidebar.text('全體客戶針對某一供應商的購買記錄')
    s_total_purchase = st.sidebar.multiselect('供應商', df['S_name'].unique())


    st.sidebar.write(df[df['S_name'].isin(s_total_purchase)])
    st.sidebar.text('總金額')
    st.sidebar.text(df[df['S_name'].isin(s_total_purchase)]['TotalPurchase'].sum())

    st.sidebar.text('===================================')
    st.sidebar.text('客戶購買總金額')
    c_total_purchase = st.sidebar.text_input('請輸入客戶ID', '')

    # st.sidebar.write(df[(df['C_ID'] == c_total_purchase)])
    # st.sidebar.text('總金額')
    # st.sidebar.text(df[(df['C_ID'] == c_total_purchase)]['TotalPurchase'].sum())
    flag = len(list(df[(df['C_ID'] == c_total_purchase)]['NotFreezingClient']))
    print('lens: ',flag)
    if flag:
        st.sidebar.write(df[(df['C_ID'] == c_total_purchase)])
        st.sidebar.text('總金額')
        st.sidebar.text(df[(df['C_ID'] == c_total_purchase)]['TotalPurchase'].sum())
    else:
        st.sidebar.write(df[(df['FC_ID'] == c_total_purchase)])
        st.sidebar.text('總金額')
        st.sidebar.text(df[(df['FC_ID'] == c_total_purchase)]['TotalPurchase'].sum())
        

    st.sidebar.text('===================================')
    st.sidebar.text('全體客戶購買總金額')
    st.sidebar.text(df['TotalPurchase'].sum())

    st.sidebar.text('===================================')
    st.sidebar.text('客戶購買排序')

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
    st.sidebar.write(client_df)

    st.sidebar.text('===================================')
    st.sidebar.text('尚未出貨')
    fas_wait = df[df['ActualDeliveryDate'] == '']
    st.sidebar.write(fas_wait)










