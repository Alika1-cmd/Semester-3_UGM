import pandas as pd
import matplotlib.pyplot as plt

# Baca CSV
df = pd.read_csv("jumlah_lembaga_per_jenjang_10provinsi.csv")

print("Data dari CSV:")
print(df.head())

# Agregasi jumlah per jenjang (total semua provinsi)
jenjang_totals = df.drop(columns=["Provinsi"]).sum().reset_index()
jenjang_totals.columns = ["Jenjang Pendidikan", "Jumlah"]

print("\nTabel Total per Jenjang:")
print(jenjang_totals)

# Grafik Bar
plt.figure(figsize=(10,6))
plt.bar(jenjang_totals["Jenjang Pendidikan"], jenjang_totals["Jumlah"], color="skyblue")
plt.title("Jumlah Satuan Pendidikan Kemenag (2024) per Jenjang - Bar Chart")
plt.xlabel("Jenjang Pendidikan")
plt.ylabel("Jumlah")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Grafik Line
plt.figure(figsize=(10,6))
plt.plot(jenjang_totals["Jenjang Pendidikan"], jenjang_totals["Jumlah"], marker="o", linestyle="-", color="green")
plt.title("Jumlah Satuan Pendidikan Kemenag (2024) per Jenjang - Line Chart")
plt.xlabel("Jenjang Pendidikan")
plt.ylabel("Jumlah")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Grafik Pie
plt.figure(figsize=(7,7))
plt.pie(jenjang_totals["Jumlah"], labels=jenjang_totals["Jenjang Pendidikan"], autopct="%1.1f%%", startangle=90)
plt.title("Persentase Satuan Pendidikan Kemenag (2024) per Jenjang - Pie Chart")
plt.show()
