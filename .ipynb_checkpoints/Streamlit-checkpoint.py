import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Data Scraping")

st.header("Raw Datas")
data = pd.read_csv("test.csv")
st.dataframe(data)

st.header("Graphics")
TotalScan = 7251
AllAges = round(36 / TotalScan * 100, 2)
Youth10 = round((11 + 593) / TotalScan * 100, 2)
Teen12 = round(2566 / TotalScan * 100, 2)
Teen13 = round(61 / TotalScan * 100, 2)
Teen14 = round(3297 / TotalScan * 100, 2)
Teen16 = round((18 + 413) / TotalScan * 100, 2)

Total = AllAges + Youth10 + Teen12 + Teen13 + Teen14 + Teen16
Reste = round(100 - Total, 2)
arr = [AllAges,Teen13, Youth10, Teen12,  Teen14, Teen16, Reste]

names=['All Ages', 'Teen(13+)', 'Youth(10+)','12+', 'Older Teen (16+)', '14+','Reste']
labels = names

fig, ax = plt.subplots()
ax.pie(arr, labels=labels, labeldistance=1.15);

st.pyplot(fig)