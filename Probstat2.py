# === games_charts.py ===
# Buat 6 grafik dari dataset penjualan video game
# Kolom wajib:
# Rank,Name,Platform,Year,Genre,Publisher,NA_Sales,EU_Sales,JP_Sales,Other_Sales,Global_Sales

import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==== Konfigurasi dasar ====
CSV_PATH = "C:/PythonSemester1/ProTis/vgsales.csv"      # ganti jika perlu
OUTPUT_DIR = "figures"      # folder untuk menyimpan gambar
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==== Load & pembersihan data ====
df = pd.read_csv(CSV_PATH)

# Pastikan kolom numerik benar
num_cols = ["NA_Sales","EU_Sales","JP_Sales","Other_Sales","Global_Sales","Year","Rank"]
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

# Drop baris tanpa penjualan global
df = df.dropna(subset=["Global_Sales"])
# Isi NaN penjualan region dengan 0
for c in ["NA_Sales","EU_Sales","JP_Sales","Other_Sales"]:
    if c in df.columns:
        df[c] = df[c].fillna(0)

# ==== Helper umum ====
def savefig(name):
    path = os.path.join(OUTPUT_DIR, name)
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Saved: {path}")

# ---------------------------------------------
# 1) Side-by-Side Horizontal Bars
#    Bandingkan penjualan NA/EU/JP untuk Top-N game berdasarkan Global_Sales
# ---------------------------------------------
def side_by_side_horizontal_bars(top_n=12):
    reg_cols = ["NA_Sales","EU_Sales","JP_Sales"]
    top = df.sort_values("Global_Sales", ascending=False).head(top_n).copy()
    top = top.iloc[::-1]  # balik agar ranking naik ke atas
    y = np.arange(len(top))
    height = 0.2

    plt.figure(figsize=(10, 6))
    for i, col in enumerate(reg_cols):
        plt.barh(y + (i-1)*height, top[col].values, height=height, label=col)

    plt.yticks(y, top["Name"].astype(str).str.slice(0, 30))
    plt.xlabel("Sales (millions)")
    plt.title(f"Top {top_n} Games – Regional Sales (Side-by-Side)")
    plt.legend()
    savefig("1_side_by_side_horizontal_bars.png")
    plt.close()

def radar_spider(top_k_genres=5):
    reg_cols = ["NA_Sales","EU_Sales","JP_Sales","Other_Sales"]
    genre_agg = df.groupby("Genre")[reg_cols + ["Global_Sales"]].sum().sort_values("Global_Sales", ascending=False)
    genres = genre_agg.head(top_k_genres).index.tolist()

    # Data radar langsung pakai angka penjualan (bukan scaling)
    vals = genre_agg.loc[genres, reg_cols].copy()

    labels = reg_cols
    N = len(labels)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # tutup loop

    plt.figure(figsize=(8,8))
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10, weight="bold")

    # Tentukan batas radial dari data
    r_max = vals.max().max()
    step = r_max / 5   # bagi jadi 5 lingkaran
    yticks = np.arange(0, r_max + step, step)

    ax.set_yticks(yticks)
    ax.set_yticklabels([f"{y:.0f}" for y in yticks], fontsize=9)
    ax.set_ylim(0, r_max)

    for g in genres:
        data = vals.loc[g].tolist()
        data += data[:1]

        ax.plot(angles, data, marker="o", label=g)
        ax.fill(angles, data, alpha=0.1)

    plt.title(f"Radar – Regional Sales Profile by Genre (Top {top_k_genres})", fontsize=12, pad=20)
    plt.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
    savefig("2_radar_spider_genre_with_radial_ticks.png")
    plt.close()


# ---------------------------------------------
# 3) Stacked horizontal bars
#    Breakdown penjualan regional untuk Top-N Publisher berdasarkan Global Sales
# ---------------------------------------------
def stacked_horizontal_bars_publishers(top_n=10):
    reg_cols = ["NA_Sales","EU_Sales","JP_Sales","Other_Sales"]
    pub_agg = df.groupby("Publisher")[reg_cols + ["Global_Sales"]].sum().sort_values("Global_Sales", ascending=False).head(top_n)
    pub_agg = pub_agg.iloc[::-1]  # agar yang terbesar di atas (dengan bar horizontal)
    y = np.arange(len(pub_agg))

    plt.figure(figsize=(10, 6))
    left = np.zeros(len(pub_agg))
    for col in reg_cols:
        plt.barh(y, pub_agg[col].values, left=left, label=col)
        left += pub_agg[col].values

    plt.yticks(y, pub_agg.index.astype(str).str.slice(0, 30))
    plt.xlabel("Sales (millions)")
    plt.title(f"Publishers – Regional Sales Breakdown (Stacked) – Top {top_n}")
    plt.legend()
    savefig("3_stacked_horizontal_bars_publishers.png")
    plt.close()

# ---------------------------------------------
# 4) 100% stacked (Likert-style) horizontal bars
#    Normalisasi per publisher menjadi persentase (%)
# ---------------------------------------------
def hundred_percent_stacked_publishers(top_n=10):
    reg_cols = ["NA_Sales","EU_Sales","JP_Sales","Other_Sales"]
    pub_agg = df.groupby("Publisher")[reg_cols + ["Global_Sales"]].sum().sort_values("Global_Sales", ascending=False).head(top_n)
    shares = pub_agg[reg_cols].div(pub_agg[reg_cols].sum(axis=1), axis=0).fillna(0)
    shares = shares.iloc[::-1]  # tampilkan besar ke atas
    y = np.arange(len(shares))

    plt.figure(figsize=(10, 6))
    left = np.zeros(len(shares))
    for col in reg_cols:
        plt.barh(y, shares[col].values*100, left=left, label=col)
        left += shares[col].values*100

    plt.yticks(y, shares.index.astype(str).str.slice(0, 30))
    plt.xlabel("Share (%)")
    plt.xlim(0, 100)
    plt.title(f"Publishers – 100% Stacked Regional Sales Share – Top {top_n}")
    plt.legend(loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.18))
    savefig("4_100pct_stacked_horizontal_bars_publishers.png")
    plt.close()

# ---------------------------------------------
# 5) Word cloud (quick qualitative summary)
#    Word cloud Genre (dibobot dengan Global_Sales)
# ---------------------------------------------
def word_cloud_genre():
    try:
        from wordcloud import WordCloud
    except ImportError:
        print("Paket 'wordcloud' belum terpasang. Jalankan: pip install wordcloud")
        return

    # Bobot: total Global_Sales per Genre
    weights = df.groupby("Genre")["Global_Sales"].sum().to_dict()
    # WordCloud menerima frekuensi dict {word: weight}
    wc = WordCloud(width=1200, height=600, background_color="white")
    wc.generate_from_frequencies(weights)

    plt.figure(figsize=(12,6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("Word Cloud – Genres (weighted by Global Sales)")
    savefig("5_wordcloud_genre.png")
    plt.close()

# ---------------------------------------------
# 6) Dumbbell (before–after) chart
#    Bandingkan NA vs EU sales untuk Top-N game (berdasarkan Global Sales)
# ---------------------------------------------
def dumbbell_na_eu(top_n=15):
    cols_needed = ["Name","NA_Sales","EU_Sales","Global_Sales"]
    data = df[cols_needed].dropna().copy()
    top = data.sort_values("Global_Sales", ascending=False).head(top_n).copy()
    top = top.iloc[::-1]  # besar ke atas dalam barh

    y = np.arange(len(top))
    plt.figure(figsize=(10, 6))

    # garis penghubung
    for i, row in top.iterrows():
        x1 = row["NA_Sales"]
        x2 = row["EU_Sales"]
        plt.plot([x1, x2], [i, i], linewidth=2)

    # titik NA & EU
    plt.scatter(top["NA_Sales"], y, s=40, label="NA_Sales", zorder=3)
    plt.scatter(top["EU_Sales"], y, s=40, label="EU_Sales", zorder=3, marker="s")

    plt.yticks(y, top["Name"].astype(str).str.slice(0, 30))
    plt.xlabel("Sales (millions)")
    plt.title(f"Dumbbell – NA vs EU Sales (Top {top_n} Games)")
    plt.legend()
    savefig("6_dumbbell_na_eu.png")
    plt.close()

# ==== Jalankan semua ====
if __name__ == "__main__":
    side_by_side_horizontal_bars(top_n=12)
    radar_spider(top_k_genres=5)
    stacked_horizontal_bars_publishers(top_n=10)
    hundred_percent_stacked_publishers(top_n=10)
    word_cloud_genre()
    dumbbell_na_eu(top_n=15)

    print("\nSelesai. Lihat folder 'figures' untuk semua gambar PNG.")
