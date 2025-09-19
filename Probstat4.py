# Hitung Koefisien Korelasi & Persamaan Regresi Linier
import pandas as pd
import numpy as np
from scipy import stats

# Baca CSV
df = pd.read_csv("games.csv")

# Pilih variabel yang berkaitan
x = df["NA_Sales"]
y = df["Global_Sales"]

# Hitung koefisien korelasi
corr_coef = x.corr(y)
print("Koefisien Korelasi:", corr_coef)

# Regresi linier (scipy)
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

print("Persamaan Regresi Linier: y = {:.4f}x + {:.4f}".format(slope, intercept))
print("R-squared:", r_value**2)

Konfirmasi Hasil (manual pakai numpy polyfit)
# polyfit orde 1 = regresi linier
m, c = np.polyfit(x, y, 1)

print("Hasil polyfit: y = {:.4f}x + {:.4f}".format(m, c))

# Plot Data + Garis Regresi Linier

import matplotlib.pyplot as plt

# Scatter plot data asli
plt.scatter(x, y, color="blue", alpha=0.5, label="Data Asli")

# Garis regresi (pakai slope & intercept dari linregress)
y_pred = intercept + slope * x
plt.plot(x, y_pred, color="red", label="Regresi Linier")

plt.title("Regresi Linier: NA_Sales vs Global_Sales")
plt.xlabel("NA_Sales")
plt.ylabel("Global_Sales")
plt.legend()
plt.grid(True)
plt.show()
