# Hitung Mean, Median, Mode, Variability, dan Standard Deviatio 
import pandas as pd
import numpy as np
from scipy import stats

# Baca CSV
df = pd.read_csv("C:/PythonSemester1/ProTis/vgsales.csv")

# Pilih hanya kolom numerik (penjualan dan tahun)
numeric_cols = ["Year","NA_Sales","EU_Sales","JP_Sales","Other_Sales","Global_Sales"]

# Statistik dasar
mean = df[numeric_cols].mean()
median = df[numeric_cols].median()
mode = df[numeric_cols].mode().iloc[0]   # ambil mode pertama
variance = df[numeric_cols].var()
std_dev = df[numeric_cols].std()

# Tampilkan hasil
print("=== Mean ===")
print(mean)
print("\n=== Median ===")
print(median)
print("\n=== Mode ===")
print(mode)
print("\n=== Variance ===")
print(variance)
print("\n=== Standard Deviation ===")
print(std_dev)

# Buat Grafik Box Plot (Box and Whisker Plot) 

import matplotlib.pyplot as plt

# Daftar kolom numerik tanpa Year
numeric_cols_no_year = ["NA_Sales","EU_Sales","JP_Sales","Other_Sales","Global_Sales"]

# Plot boxplot untuk semua kolom numerik (tanpa Year)
df[numeric_cols_no_year].plot(kind='box', figsize=(10,6))

plt.title("Box and Whisker Plot - Game Sales Data (tanpa Year)")
plt.ylabel("Values (millions)")
plt.grid(True)
plt.show()

