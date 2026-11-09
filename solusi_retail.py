#!/usr/bin/env python3
"""Retail crisis/recovery analysis for the DQLab hackathon.

Reads sales_transaction.csv or data_penjualan.csv from the working directory and
writes retail_insight.xlsx, rising_star_index.png, and rising_star_actual.png.
"""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


INPUT_CANDIDATES = ("sales_transaction.csv", "data_penjualan.csv")
OUTPUT_EXCEL = "retail_insight.xlsx"
REQUIRED_COLUMNS = {
    "nomor_struk",
    "tgl_transaksi",
    "kode_produk",
    "nama_produk",
    "jumlah_terjual",
    "harga",
    "total_nilai",
}
WINDOW_DAYS = 3
MIN_CONSECUTIVE_RISES = 12
MIN_SUPPORT = 0.01
MIN_LIFT = 2.0


def load_transactions() -> pd.DataFrame:
    """Load the first available CSV, allowing comma or semicolon delimiters."""
    input_path = next((Path(name) for name in INPUT_CANDIDATES if Path(name).is_file()), None)
    if input_path is None:
        names = " or ".join(INPUT_CANDIDATES)
        raise FileNotFoundError(f"Input CSV not found. Place {names} in the working directory.")

    errors: list[str] = []
    for delimiter in (None, ";", ","):
        try:
            if delimiter is None:
                frame = pd.read_csv(input_path, sep=None, engine="python", encoding="utf-8-sig")
            else:
                frame = pd.read_csv(input_path, sep=delimiter, encoding="utf-8-sig")
            frame.columns = frame.columns.astype(str).str.strip()
            if REQUIRED_COLUMNS.issubset(frame.columns):
                break
        except Exception as exc:  # try the next common delimiter
            errors.append(str(exc))
    else:
        present = ", ".join(map(str, frame.columns)) if "frame" in locals() else "unavailable"
        raise ValueError(
            f"Could not parse {input_path} with required columns. Found columns: {present}. "
            f"Required: {', '.join(sorted(REQUIRED_COLUMNS))}. {errors}"
        )

    frame = frame.copy()
    frame["tgl_transaksi"] = pd.to_datetime(frame["tgl_transaksi"], errors="coerce", dayfirst=True)
    for column in ("jumlah_terjual", "harga", "total_nilai"):
        frame[column] = pd.to_numeric(frame[column], errors="coerce")

    frame = frame.dropna(
        subset=["nomor_struk", "tgl_transaksi", "kode_produk", "nama_produk", "jumlah_terjual", "total_nilai"]
    )
    if frame.empty:
        raise ValueError(f"No valid transaction rows were found in {input_path}.")
    frame["tgl_transaksi"] = frame["tgl_transaksi"].dt.normalize()
    return frame


def build_daily_series(transactions: pd.DataFrame) -> pd.DataFrame:
    """Create a complete calendar-day series per SKU and compute its 3-day MA."""
    daily = (
        transactions.groupby(["kode_produk", "nama_produk", "tgl_transaksi"], as_index=False)["total_nilai"]
        .sum()
    )
    all_days = pd.date_range(daily["tgl_transaksi"].min(), daily["tgl_transaksi"].max(), freq="D")
    products: list[pd.DataFrame] = []
    for (code, name), group in daily.groupby(["kode_produk", "nama_produk"], sort=False):
        series = group.set_index("tgl_transaksi")["total_nilai"].reindex(all_days, fill_value=0)
        item = series.rename("total_nilai").rename_axis("tgl_transaksi").reset_index()
        item["kode_produk"] = code
        item["nama_produk"] = name
        item["MA"] = item["total_nilai"].rolling(WINDOW_DAYS, min_periods=WINDOW_DAYS).mean()
        products.append(item)
    return pd.concat(products, ignore_index=True)


def find_rising_stars(daily: pd.DataFrame, transactions: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Find products with at least 12 consecutive day-over-day MA increases."""
    daily = daily.copy()
    daily["MA_change"] = daily.groupby("kode_produk", sort=False)["MA"].diff()
    daily["is_rising"] = daily["MA_change"].gt(0).fillna(False)

    rising_rows: list[dict] = []
    for (code, name), group in daily.groupby(["kode_produk", "nama_produk"], sort=False):
        group = group.reset_index(drop=True)
        run_length = 0
        for index, is_rising in enumerate(group["is_rising"]):
            run_length = run_length + 1 if is_rising else 0
            if is_rising and run_length >= MIN_CONSECUTIVE_RISES:
                start_index = index - run_length
                start_ma = group.loc[start_index, "MA"]
                end_ma = group.loc[index, "MA"]
                if pd.notna(start_ma) and start_ma != 0:
                    rising_rows.append(
                        {
                            "kode_produk": code,
                            "nama_produk": name,
                            "session_start": group.loc[start_index + 1, "tgl_transaksi"],
                            "session_end": group.loc[index, "tgl_transaksi"],
                            "consecutive_rises": run_length,
                            "growth_pct": (end_ma / start_ma - 1) * 100,
                        }
                    )

    total_sales = (
        transactions.groupby(["kode_produk", "nama_produk"], as_index=False)["total_nilai"]
        .sum()
        .rename(columns={"total_nilai": "total_sales"})
    )
    sessions = pd.DataFrame(
        rising_rows,
        columns=["kode_produk", "nama_produk", "session_start", "session_end", "consecutive_rises", "growth_pct"],
    )
    if sessions.empty:
        report = pd.DataFrame(columns=["kode_produk", "nama_produk", "growth_pct", "total_sales", "consecutive_rises", "session_start", "session_end"])
    else:
        # Keep the strongest qualifying session for each product for a concise product-level report.
        sessions = sessions.sort_values(["growth_pct", "consecutive_rises"], ascending=[False, False])
        best_sessions = sessions.drop_duplicates("kode_produk", keep="first")
        report = best_sessions.merge(total_sales, on=["kode_produk", "nama_produk"], how="left")
        report = report.sort_values("growth_pct", ascending=False).reset_index(drop=True)
    return report, daily


def build_packaging(transactions: pd.DataFrame, rising_star_names: set[str]) -> pd.DataFrame:
    """Mine association rules and retain high-lift rules containing a Rising Star."""
    columns = ["Jika Membeli", "Maka Membeli", "Jumlah Invoice", "Support", "Confidence", "Lift"]
    basket = (
        transactions.groupby(["nomor_struk", "nama_produk"])["jumlah_terjual"]
        .sum()
        .unstack(fill_value=0)
        .gt(0)
    )
    if basket.empty or basket.shape[1] < 2 or not rising_star_names:
        return pd.DataFrame(columns=columns)

    itemsets = apriori(basket, min_support=MIN_SUPPORT, use_colnames=True)
    if itemsets.empty:
        return pd.DataFrame(columns=columns)
    rules = association_rules(itemsets, metric="lift", min_threshold=1.0)
    if rules.empty:
        return pd.DataFrame(columns=columns)

    contains_rising_star = rules["antecedents"].apply(lambda items: bool(set(items) & rising_star_names)) | rules[
        "consequents"
    ].apply(lambda items: bool(set(items) & rising_star_names))
    rules = rules.loc[contains_rising_star & rules["lift"].ge(MIN_LIFT)].copy()
    if rules.empty:
        return pd.DataFrame(columns=columns)

    total_transactions = basket.shape[0]
    rules["Jumlah Invoice"] = (rules["support"] * total_transactions).round().astype(int)
    result = pd.DataFrame(
        {
            "Jika Membeli": rules["antecedents"].apply(lambda items: ", ".join(sorted(items))),
            "Maka Membeli": rules["consequents"].apply(lambda items: ", ".join(sorted(items))),
            "Jumlah Invoice": rules["Jumlah Invoice"],
            "Support": rules["support"],
            "Confidence": rules["confidence"],
            "Lift": rules["lift"],
        }
    )
    return result.sort_values(["Lift", "Support", "Confidence"], ascending=False).reset_index(drop=True)


def plot_reports(daily: pd.DataFrame, report: pd.DataFrame, transactions: pd.DataFrame) -> None:
    """Write indexed MA and actual daily sales charts, including the top 3 SKUs."""
    palette = ["#FFD700", "#C0C0C0", "#CD7F32", "#2ecc71", "#3498db", "#9b59b6", "#e74c3c", "#34495e"]
    gray_palette = ["#B0B0B0", "#909090", "#707070"]
    stars = report["kode_produk"].tolist() if not report.empty else []
    revenue_rank = (
        transactions.groupby(["kode_produk", "nama_produk"], as_index=False)["total_nilai"]
        .sum()
        .sort_values("total_nilai", ascending=False)
    )
    top3 = revenue_rank.head(3)

    def normalized(group: pd.DataFrame, value_column: str) -> pd.Series:
        values = group[value_column]
        valid = values.dropna()
        if valid.empty or valid.iloc[0] == 0:
            return pd.Series(float("nan"), index=group.index)
        first = valid.iloc[0]
        return values / first * 100

    fig, ax = plt.subplots(figsize=(15, 8), dpi=100)
    for index, row in enumerate(top3.itertuples(index=False)):
        group = daily[daily["kode_produk"].eq(row.kode_produk)].sort_values("tgl_transaksi")
        y = normalized(group, "MA")
        ax.plot(group["tgl_transaksi"], y, linestyle="--", linewidth=2, marker="o", markersize=3,
                color=gray_palette[index], alpha=0.7, label=f"Top Sales: {row.nama_produk}")
    for rank, code in enumerate(stars, start=1):
        group = daily[daily["kode_produk"].eq(code)].sort_values("tgl_transaksi")
        if group.empty:
            continue
        y = normalized(group, "MA")
        ax.plot(group["tgl_transaksi"], y, marker="o", markersize=4, linewidth=2.5,
                color=palette[(rank - 1) % len(palette)], label=f"Rank {rank}: {group['nama_produk'].iloc[0]}")
    ax.set_title("ANALISIS PERTUMBUHAN RELATIF PRODUK RISING STAR\n(Dengan Benchmark Top 3 Total Penjualan)",
                 fontdict={"family": "sans-serif", "color": "black", "weight": "bold", "size": 16}, pad=20)
    ax.set_xlabel("Periode Tanggal", fontsize=12, labelpad=10)
    ax.set_ylabel("Indeks Pertumbuhan (Base 100)", fontsize=12, labelpad=10)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
    ax.axhline(100, color="black", linewidth=1, alpha=0.5)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=10)
    ax.legend(title="Kategori Produk", fontsize=9, title_fontsize=11, bbox_to_anchor=(1.02, 1), loc="upper left", shadow=True)
    fig.tight_layout()
    fig.savefig("rising_star_index.png", bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(15, 8), dpi=100)
    for index, row in enumerate(top3.itertuples(index=False)):
        group = daily[daily["kode_produk"].eq(row.kode_produk)].sort_values("tgl_transaksi")
        ax.plot(group["tgl_transaksi"], group["total_nilai"], linestyle="--", linewidth=2, marker="o", markersize=3,
                color=gray_palette[index], alpha=0.7, label=f"Top Sales: {row.nama_produk}")
    for rank, code in enumerate(stars, start=1):
        group = daily[daily["kode_produk"].eq(code)].sort_values("tgl_transaksi")
        if group.empty:
            continue
        ax.plot(group["tgl_transaksi"], group["total_nilai"], marker="o", markersize=4, linewidth=2.5,
                color=palette[(rank - 1) % len(palette)], label=f"Rank {rank}: {group['nama_produk'].iloc[0]}")
    ax.set_title("ANALISIS NILAI PENJUALAN PRODUK RISING STAR\n(Nilai Penjualan Asli)",
                 fontdict={"family": "sans-serif", "color": "black", "weight": "bold", "size": 16}, pad=20)
    ax.set_xlabel("Periode Tanggal", fontsize=12, labelpad=10)
    ax.set_ylabel("Total Nilai Penjualan", fontsize=12, labelpad=10)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=10)
    ax.legend(title="Kategori Produk", fontsize=9, title_fontsize=11, bbox_to_anchor=(1.02, 1), loc="upper left", shadow=True)
    fig.tight_layout()
    fig.savefig("rising_star_actual.png", bbox_inches="tight")
    plt.close(fig)


def write_excel(report: pd.DataFrame, packaging: pd.DataFrame) -> None:
    rising_output = report.rename(
        columns={
            "kode_produk": "Kode Produk",
            "nama_produk": "Nama Produk",
            "growth_pct": "Growth %",
            "total_sales": "Total Penjualan",
            "consecutive_rises": "Kenaikan Berturut-turut",
            "session_start": "Awal Sesi",
            "session_end": "Akhir Sesi",
        }
    )
    with pd.ExcelWriter(OUTPUT_EXCEL, engine="openpyxl") as writer:
        rising_output.to_excel(writer, sheet_name="Rising Star", index=False)
        packaging.to_excel(writer, sheet_name="Potential Packaging", index=False)
        for worksheet in writer.book.worksheets:
            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions
            for cell in worksheet[1]:
                cell.font = cell.font.copy(bold=True)
            for cells in worksheet.columns:
                width = max((len(str(cell.value)) if cell.value is not None else 0) for cell in cells)
                worksheet.column_dimensions[cells[0].column_letter].width = min(width + 2, 48)


def main() -> int:
    try:
        transactions = load_transactions()
        daily = build_daily_series(transactions)
        report, daily = find_rising_stars(daily, transactions)
        packaging = build_packaging(transactions, set(report["nama_produk"]))
        write_excel(report, packaging)
        plot_reports(daily, report, transactions)
    except Exception as exc:
        print(f"Analysis failed: {exc}", file=sys.stderr)
        return 1

    print(f"Loaded {len(transactions):,} transaction lines.")
    print(f"Found {len(report):,} Rising Star product(s) and {len(packaging):,} packaging rule(s).")
    print(f"Created {OUTPUT_EXCEL}, rising_star_index.png, and rising_star_actual.png.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
