# 界面构建
import streamlit as st
import altair as alt
from streamlit_autorefresh import st_autorefresh

# 资料结构
import pandas as pd
import numpy as np
# mysql引擎
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#正规时间
import time 
#正则match
import re 
# 图片读取
from PIL import Image
# 数据流
from io import BytesIO


# 主方法
from database import *
# 分页
from subpages.page_client import *
from subpages.page_client_purchase import *
from subpages.page_fas import *
from subpages.page_freezing_client import *
from subpages.page_supplier import *

# st_refresh_count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

st.set_page_config(
    page_title = "Flower & Seedling Database System",
    page_icon = "🌸",
    layout="wide",
    initial_sidebar_state="expanded",
    
)
st.sidebar.title("蒙德花園") #sidebar 標題

Database_table = st.sidebar.selectbox( #資料庫選擇
    "資料庫",
    ("花草苗木資料表", "客戶資料表", "靜止戶資料表","供應商資料表","客戶購買資料表")
)

if Database_table=="花草苗木資料表":
    page_fas()

if Database_table=="客戶資料表":
    page_client()

if Database_table=="靜止戶資料表":
    page_freezing_client()


if Database_table=="供應商資料表":
    page_supplier()

if Database_table=="客戶購買資料表":
    page_client_purchase()
