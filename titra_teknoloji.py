# -*- coding: utf-8 -*-
"""Titra_Teknoloji

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JH6ZDROE1hC697KQQDqpCQxfO8XkjPui

Importing Libraries
"""

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from yellowbrick.cluster import KElbowVisualizer
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from sklearn.preprocessing import StandardScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', 20)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

"""Some functions

"""

def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

def grab_col_names(dataframe, cat_th=10, car_th=20):
    """

    Veri setindeki kategorik, numerik ve kategorik fakat kardinal değişkenlerin isimlerini verir.
    Not: Kategorik değişkenlerin içerisine numerik görünümlü kategorik değişkenler de dahildir.

    Parameters
    ------
        dataframe: dataframe
                Değişken isimleri alınmak istenilen dataframe
        cat_th: int, optional
                numerik fakat kategorik olan değişkenler için sınıf eşik değeri
        car_th: int, optinal
                kategorik fakat kardinal değişkenler için sınıf eşik değeri

    Returns
    ------
        cat_cols: list
                Kategorik değişken listesi
        num_cols: list
                Numerik değişken listesi
        cat_but_car: list
                Kategorik görünümlü kardinal değişken listesi

    Examples
    ------
        import seaborn as sns
        df = sns.load_dataset("iris")
        print(grab_col_names(df))


    Notes
    ------
        cat_cols + num_cols + cat_but_car = toplam değişken sayısı
        num_but_cat cat_cols'un içerisinde.
        Return olan 3 liste toplamı toplam değişken sayısına eşittir: cat_cols + num_cols + cat_but_car = değişken sayısı

    """

     # cat_cols, cat_but_car
    cat_cols = [col for col in dataframe.columns if dataframe[col].dtypes == "O"]
    num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique() < cat_th and
                   dataframe[col].dtypes != "O"]
    cat_but_car = [col for col in dataframe.columns if dataframe[col].nunique() > car_th and
                   dataframe[col].dtypes == "O"]
    cat_cols = cat_cols + num_but_cat
    cat_cols = [col for col in cat_cols if col not in cat_but_car]

    # num_cols
    num_cols = [col for col in dataframe.columns if dataframe[col].dtypes != "O"]
    num_cols = [col for col in num_cols if col not in num_but_cat]

    # print(f"Observations: {dataframe.shape[0]}")
    # print(f"Variables: {dataframe.shape[1]}")
    # print(f'cat_cols: {len(cat_cols)}')
    # print(f'num_cols: {len(num_cols)}')
    # print(f'cat_but_car: {len(cat_but_car)}')
    # print(f'num_but_cat: {len(num_but_cat)}')
    return cat_cols, num_cols, cat_but_car

def correlation_matrix(df, cols):
    fig = plt.gcf()
    fig.set_size_inches(10, 8)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    fig = sns.heatmap(df[cols].corr(), annot=True, linewidths=0.5, annot_kws={'size': 12}, linecolor='w', cmap='RdBu')
    plt.show(block=True)

df_ang_vel = pd.read_csv("/content/drive/MyDrive/titra/angular_velocity.csv")

df_fly = pd.read_csv("/content/drive/MyDrive/titra/flight.csv")

df_gps = pd.read_csv("/content/drive/MyDrive/titra/gps.csv")

df_ang_vel["a"]=df_ang_vel["xyz[0]"]/df_ang_vel["xyz[1]"]

df_ang_vel["b"]=df_ang_vel["xyz[1]"]/df_ang_vel["xyz[0]"]

df_ang_vel=df_ang_vel[(df_ang_vel["a"]>1.3) | (df_ang_vel["b"]>1.3)]

check_df(df_ang_vel)

"""change the type of timestamp column for plotting

"""

df_ang_vel['time'] = pd.to_datetime(df_ang_vel['time'])

df_ang_vel['time']=df_ang_vel['time'].dt.strftime('%f')

df_ang_vel["time"]=df_ang_vel["time"].astype("int64")

df_ang_vel.info()

cat_cols, num_cols, cat_but_car = grab_col_names(df_ang_vel, cat_th=5, car_th=20)

correlation_matrix(df_ang_vel, num_cols)

df_fly.head()

check_df(df_fly)

df_gps.head()

check_df(df_gps)

df_gps.info()

df_gps['time'] = pd.to_datetime(df_gps['time'])

df_gps['time']=df_gps['time'].dt.strftime('%f')

df_gps["time"]=df_gps["time"].astype("int64")

df_gps.info()

df_ang_vel.info()

df = pd.merge(df_ang_vel,df_gps,on=["time","flight_id"],how='inner')

df.head()

check_df(df)

"""#PCA"""

numcols=[i for i in df.columns if df[i].dtypes != "O" and "flight_id" not in i]

df=df[numcols]

df.isnull().sum()

df = StandardScaler().fit_transform(df)

pca = PCA()

pca_fit = pca.fit_transform(df)

pca.explained_variance_ratio_

np.cumsum(pca.explained_variance_ratio_)

"""# OPTIMUM BILESEN SAYISI"""

pca = PCA().fit(df)
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel("Bileşen Sayısını")
plt.ylabel("Kümülatif Varyans Oranı")
plt.show(block=True)

"""#FINAL PCA"""

pca = PCA(n_components=3)

pca_fit = pca.fit_transform(df)

pca.explained_variance_ratio_

np.cumsum(pca.explained_variance_ratio_)

"""DASHBOARD"""

df = pd.merge(df_ang_vel,df_gps,on=["time","flight_id"],how='inner')

df.head()

pip install streamlit

import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # data web app development

st.set_page_config(
    page_title="Data Science Dashboard",
    page_icon="✅",
    layout="wide")

"""dashboard title"""

st.title("Data Science Dashboard")

"""top-level filters"""

flight_filter = st.selectbox("Select the Flight", pd.unique(df["flight_id"]))

"""dataframe filter"""

df = df[df["flight_id"] == flight_filter]

"""create two columns for charts"""

fig_col1,fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### First Chart")
    fig = px.density_heatmap(
        data_frame=df, y="flight_id", x="time"
    )
    st.write(fig)

with fig_col2:
    st.markdown("### Second Chart")
    fig2 = px.scatter_3d(df, x='lat', y='lon', z='alt',
              color='flight_id')
    st.write(fig2)

st.markdown("### Detailed Data View")
st.dataframe(df)

placeholder = st.empty()

# near real-time / live feed simulation
for seconds in range(200):

    df["flight_id_new"] = df["flight_id"] * np.random.choice(range(1, 5))
    df["time_new"] = df["time"] * np.random.choice(range(1, 5))


    with placeholder.container():


        # create two columns for charts
        fig_col1,fig_col2 = st.columns(2)


    with fig_col1:
        st.markdown("### First Chart")
        fig = px.density_heatmap(
            data_frame=df, y="flight_id", x="time"
        )
        st.write(fig)

    with fig_col2:
        st.markdown("### Second Chart")
        fig2 = px.scatter_3d(df, x='lat', y='lon', z='alt',
              color='flight_id')
        st.write(fig2)

        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)