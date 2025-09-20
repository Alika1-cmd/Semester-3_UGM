import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Baca CSV
df = pd.read_csv("C:/PythonSemester1/ProTis/Global_Education.csv", encoding="latin1")

# --- 1. Buat kategori dari Unemployment_Rate ---
def categorize_unemployment(rate):
    if rate < 5:
        return "Rendah"
    elif rate <= 10:
        return "Sedang"
    else:
        return "Tinggi"

df["Unemp_Category"] = df["Unemployment_Rate"].apply(categorize_unemployment)

# Frekuensi & frekuensi relatif
freq = df["Unemp_Category"].value_counts()
rel_freq = df["Unemp_Category"].value_counts(normalize=True)

print("Frekuensi Kategori Pengangguran:\n", freq)
print("\nFrekuensi Relatif:\n", rel_freq)

# --- 2. Hitung peluang tiap kategori (sama dengan frekuensi relatif) ---
probabilities = rel_freq
print("\nPeluang tiap kategori:\n", probabilities)

# --- 3. Bayes Rule ---
# Event A: Birth_Rate > 20
A = df["Birth_Rate"] > 20
P_A = A.mean()  # P(A)

print("\nP(A) (Birth Rate > 20):", P_A)

for category in df["Unemp_Category"].unique():
    numerator = len(df[(df["Unemp_Category"] == category) & (A)]) / len(df)
    P_Si_given_A = numerator / P_A if P_A > 0 else np.nan
    print(f"P({category} | A) = {P_Si_given_A:.4f}")

# --- 4. Statistik Birth_Rate ---
birth_rate = df["Birth_Rate"].dropna()
mean = birth_rate.mean()
variance = birth_rate.var()
std_dev = birth_rate.std()

print("\nStatistik Birth Rate:")
print("Mean:", mean)
print("Variance:", variance)
print("Standard Deviation:", std_dev)

# --- 5. Probability Histogram ---
plt.figure(figsize=(8,5))
plt.hist(birth_rate, bins=15, density=True, alpha=0.7, color="skyblue", edgecolor="black")
plt.title("Probability Histogram of Birth Rate")
plt.xlabel("Birth Rate")
plt.ylabel("Probability Density")
plt.grid(True)
plt.show()
