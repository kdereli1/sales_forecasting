from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs" / "OUTPUT_SARIMA"
IMAGE_DIR = ROOT / "SUNUM1" / "gorseller"
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

raw = pd.read_csv(ROOT / "data" / "complete_cleaned_data_full.csv", sep=";")
raw["sehir_adi"] = raw["sehir_adi"].astype(str).str.strip()
antalya = raw.loc[raw["sehir_adi"].eq("Antalya")].copy()
antalya["checkin"] = pd.to_datetime(antalya["voucher_checkin_date"], errors="coerce").dt.normalize()
antalya["checkout"] = pd.to_datetime(antalya["voucher_checout_date"], errors="coerce").dt.normalize()
antalya = antalya.loc[antalya["checkin"].notna() & antalya["checkout"].notna() & antalya["checkout"].gt(antalya["checkin"])].copy()

region_to_district = {
    "Acısu": "Serik", "Adrasan": "Kumluca", "Aksu": "Aksu", "Alanya": "Alanya", "Avsallar": "Alanya",
    "Beldibi": "Kemer", "Belek": "Serik", "Boğazkent": "Serik", "Çamyuva": "Kemer", "Çıralı": "Kumluca",
    "Çolaklı": "Manavgat", "Çukurbağ Yarımadası": "Kaş", "Dimçayı": "Alanya", "Döşemealtı": "Döşemealtı",
    "Evrenseki": "Manavgat", "Falez": "Muratpaşa", "Finike": "Finike", "Gazipaşa": "Gazipaşa",
    "Göynük": "Kemer", "İleribaşı Mevkii": "Serik", "İncekum": "Alanya", "İskele Mevki": "Serik",
    "Kaleiçi": "Muratpaşa", "Kalkan": "Kaş", "Kargıcak": "Alanya", "Karya Mevkii": "Serik", "Kaş": "Kaş",
    "Kemer": "Kemer", "Kepez": "Kepez", "Kestel": "Alanya", "Kiriş": "Kemer", "Kızılagaç": "Manavgat",
    "Kızılot": "Manavgat", "Konaklı": "Alanya", "Konyaaltı": "Konyaaltı", "Küçük Çakıl Mevkii": "Kaş",
    "Kumköy": "Manavgat", "Kumluca": "Kumluca", "Lara": "Muratpaşa", "Mahmutlar": "Alanya", "Manavgat": "Manavgat",
    "Merkez": "Muratpaşa", "Muratpaşa": "Muratpaşa", "Oba": "Alanya", "Obagöl": "Alanya", "Okurcalar": "Alanya",
    "Olimpos": "Kumluca", "Serik": "Serik", "Side": "Manavgat", "Sorgun": "Manavgat", "Taşlıburun": "Serik",
    "Tekirova": "Kemer", "Titreyengöl": "Manavgat", "Türkler": "Alanya", "Üç Kum Tepesi": "Serik",
}


def build_district_monthly(start, end):
    source = antalya[["hotel_region_name", "checkin", "checkout"]].copy()
    source["district"] = source["hotel_region_name"].astype("string").str.strip().map(region_to_district).fillna("Eşleşmeyen")
    source["start"] = source["checkin"].clip(lower=start)
    source["end"] = source["checkout"].clip(upper=end + pd.Timedelta(days=1))
    source = source.loc[source["end"].gt(source["start"])].copy()
    source["nights"] = (source["end"] - source["start"]).dt.days
    rows = []
    for record in source.itertuples(index=False):
        for month in pd.date_range(record.start.to_period("M").to_timestamp(), record.end.to_period("M").to_timestamp(), freq="MS"):
            month_end = month + pd.offsets.MonthBegin(1)
            overlap_start = max(record.start, month)
            overlap_end = min(record.end, month_end)
            if overlap_end > overlap_start:
                rows.append({"district": record.district, "month": month,
                             "occupied_nights": (overlap_end - overlap_start).days})
    return pd.DataFrame(rows).groupby(["district", "month"], as_index=False)["occupied_nights"].sum()


def save_clean_panels(data, group_column, prediction_column, title, filename, metric_columns):
    groups = data[group_column].drop_duplicates().tolist()
    columns = 4
    rows = int(np.ceil(len(groups) / columns))
    fig, axes = plt.subplots(rows, columns, figsize=(18, 3.8 * rows), sharex=True)
    axes = np.asarray(axes).reshape(rows, columns)
    for axis, group_name in zip(axes.flat, groups):
        part = data.loc[data[group_column].eq(group_name)].sort_values("month")
        axis.plot(part["month"], part["actual"], marker="o", linewidth=2.2, color="#1f2937", label="Gerçek")
        axis.plot(part["month"], part[prediction_column], marker="o", linestyle="--", linewidth=2.0, color="#e8590c", label="SARIMAX + düzeltme")
        axis.set_title(str(group_name), fontsize=10)
        axis.tick_params(axis="x", rotation=45, labelsize=8)
        axis.grid(alpha=0.25)
        values = [f"{label}: {part[label_column].iloc[0]:.1f}%" for label, label_column in metric_columns]
        axis.text(0.03, 0.97, "\n".join(values), transform=axis.transAxes, va="top", fontsize=8,
                  bbox={"facecolor": "white", "alpha": 0.86, "edgecolor": "#adb5bd"})
    for axis in axes.flat[len(groups):]:
        axis.set_visible(False)
    axes.flat[0].legend(fontsize=8, loc="upper right")
    fig.suptitle(title, fontsize=16, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(IMAGE_DIR / filename, dpi=180, bbox_inches="tight")
    plt.close(fig)


# 2025 district panels: fixed-order SARIMAX with training-only calendar corrections.
district_monthly_2025 = build_district_monthly(pd.Timestamp("2023-01-01"), pd.Timestamp("2025-12-31"))
district_predictions_rows = []
for district in ["Alanya", "Kaş", "Kemer", "Kumluca", "Manavgat", "Muratpaşa", "Serik"]:
    series = (district_monthly_2025.loc[district_monthly_2025["district"].eq(district)]
              .set_index("month")["occupied_nights"]
              .reindex(pd.date_range("2023-01-01", "2025-12-01", freq="MS"), fill_value=0).astype(float))
    train = series.loc["2023-01-01":"2024-12-01"]
    actual = series.loc["2025-01-01":"2025-12-01"]
    model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 0, 0, 12), trend="c",
                    enforce_stationarity=False, enforce_invertibility=False).fit(disp=False, maxiter=200)
    prediction = pd.Series(model.get_forecast(steps=12).predicted_mean.to_numpy(), index=actual.index).clip(lower=0)
    fitted = pd.Series(np.asarray(model.fittedvalues), index=train.index)
    residuals = (train - fitted).replace([np.inf, -np.inf], np.nan)
    may_uplift = max(0.0, float(residuals.loc[residuals.index.month == 5].dropna().median()))
    june_ratios = (train.loc[train.index.month == 6] / fitted.loc[fitted.index.month == 6].replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).dropna()
    june_transfer = float(np.clip(june_ratios.median(), 0.25, 1.50)) if not june_ratios.empty else 1.0
    prediction.loc["2025-05-01"] += may_uplift
    prediction.loc["2025-06-01"] *= june_transfer
    actual_total = actual.sum()
    total_error_pct = abs(prediction.sum() - actual_total) / actual_total * 100 if actual_total else np.nan
    wmape = (actual - prediction).abs().sum() / actual_total * 100 if actual_total else np.nan
    for month, actual_value, prediction_value in zip(actual.index, actual.values, prediction.values):
        district_predictions_rows.append({"district": district, "month": month, "actual": actual_value,
                                          "prediction": prediction_value, "WMAPE": wmape,
                                          "total_error_pct": total_error_pct})
district_predictions = pd.DataFrame(district_predictions_rows)
district_predictions.to_csv(OUTPUT_DIR / "sunum1_2025_district_sarimax_adjusted.csv", index=False)
district_scores = district_predictions.groupby("district", as_index=False).first()
district_scores.to_csv(OUTPUT_DIR / "sunum1_2025_district_scores_with_total_error.csv", index=False)
save_clean_panels(
    district_predictions,
    "district",
    "prediction",
    "Antalya İlçe Bazlı 2025 Backtest: Gerçek vs Seçilen Model",
    "sunum1_2025_district_clean.png",
    [("WMAPE", "WMAPE"), ("Toplam hata", "total_error_pct")],
)

# 2026 district SARIMAX + training-only calendar corrections.
raw = pd.read_csv(ROOT / "data" / "complete_cleaned_data_full.csv", sep=";")
raw["sehir_adi"] = raw["sehir_adi"].astype(str).str.strip()
antalya = raw.loc[raw["sehir_adi"].eq("Antalya")].copy()
antalya["checkin"] = pd.to_datetime(antalya["voucher_checkin_date"], errors="coerce").dt.normalize()
antalya["checkout"] = pd.to_datetime(antalya["voucher_checout_date"], errors="coerce").dt.normalize()
antalya = antalya.loc[antalya["checkin"].notna() & antalya["checkout"].notna() & antalya["checkout"].gt(antalya["checkin"])].copy()
region_to_district = {
    "Acısu": "Serik", "Adrasan": "Kumluca", "Aksu": "Aksu", "Alanya": "Alanya", "Avsallar": "Alanya",
    "Beldibi": "Kemer", "Belek": "Serik", "Boğazkent": "Serik", "Çamyuva": "Kemer", "Çıralı": "Kumluca",
    "Çolaklı": "Manavgat", "Çukurbağ Yarımadası": "Kaş", "Dimçayı": "Alanya", "Döşemealtı": "Döşemealtı",
    "Evrenseki": "Manavgat", "Falez": "Muratpaşa", "Finike": "Finike", "Gazipaşa": "Gazipaşa",
    "Göynük": "Kemer", "İleribaşı Mevkii": "Serik", "İncekum": "Alanya", "İskele Mevki": "Serik",
    "Kaleiçi": "Muratpaşa", "Kalkan": "Kaş", "Kargıcak": "Alanya", "Karya Mevkii": "Serik", "Kaş": "Kaş",
    "Kemer": "Kemer", "Kepez": "Kepez", "Kestel": "Alanya", "Kiriş": "Kemer", "Kızılagaç": "Manavgat",
    "Kızılot": "Manavgat", "Konaklı": "Alanya", "Konyaaltı": "Konyaaltı", "Küçük Çakıl Mevkii": "Kaş",
    "Kumköy": "Manavgat", "Kumluca": "Kumluca", "Lara": "Muratpaşa", "Mahmutlar": "Alanya", "Manavgat": "Manavgat",
    "Merkez": "Muratpaşa", "Muratpaşa": "Muratpaşa", "Oba": "Alanya", "Obagöl": "Alanya", "Okurcalar": "Alanya",
    "Olimpos": "Kumluca", "Serik": "Serik", "Side": "Manavgat", "Sorgun": "Manavgat", "Taşlıburun": "Serik",
    "Tekirova": "Kemer", "Titreyengöl": "Manavgat", "Türkler": "Alanya", "Üç Kum Tepesi": "Serik",
}
months = pd.date_range("2023-01-01", "2026-07-01", freq="MS")
monthly = build_district_monthly(pd.Timestamp("2023-01-01"), pd.Timestamp("2026-07-31"))
selected = ["Alanya", "Kaş", "Kemer", "Kumluca", "Manavgat", "Muratpaşa", "Serik"]
rows = []
for district in selected:
    series = (monthly.loc[monthly["district"].eq(district)].set_index("month")["occupied_nights"]
              .reindex(months, fill_value=0).astype(float))
    train = series.loc["2023-01-01":"2025-12-01"]
    actual = series.loc["2026-03-01":"2026-07-01"]
    model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 0, 0, 12), trend="c",
                    enforce_stationarity=False, enforce_invertibility=False).fit(disp=False, maxiter=200)
    baseline = pd.Series(model.get_forecast(steps=7).predicted_mean.to_numpy(), index=pd.date_range("2026-01-01", "2026-07-01")).clip(lower=0)
    fitted = pd.Series(np.asarray(model.fittedvalues), index=train.index)
    residuals = (train - fitted).replace([np.inf, -np.inf], np.nan)
    may_uplift = max(0.0, float(residuals.loc[residuals.index.month == 5].dropna().median()))
    june_ratios = (train.loc[train.index.month == 6] / fitted.loc[fitted.index.month == 6].replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).dropna()
    june_transfer = float(np.clip(june_ratios.median(), 0.25, 1.50)) if not june_ratios.empty else 1.0
    adjusted = baseline.copy()
    adjusted.loc["2026-05-01"] += may_uplift
    adjusted.loc["2026-06-01"] *= june_transfer
    predicted = adjusted.loc[actual.index]
    error = actual - predicted
    actual_total = actual.sum()
    wmape = error.abs().sum() / actual_total * 100 if actual_total else np.nan
    total_error = abs(predicted.sum() - actual_total) / actual_total * 100 if actual_total else np.nan
    for month, actual_value, prediction_value in zip(actual.index, actual.values, predicted.values):
        rows.append({"district": district, "month": month, "actual": actual_value, "prediction": prediction_value,
                     "WMAPE": wmape, "total_error_pct": total_error, "may_uplift": may_uplift,
                     "june_transfer_factor": june_transfer})
district_2026 = pd.DataFrame(rows)
district_2026.to_csv(OUTPUT_DIR / "sunum1_2026_district_sarimax_adjusted.csv", index=False)
save_clean_panels(
    district_2026,
    "district",
    "prediction",
    "Antalya İlçe Bazlı 2026 Mart-Temmuz: SARIMAX + Takvim Düzeltmesi",
    "sunum1_2026_district_sarimax_adjusted_clean.png",
    [("WMAPE", "WMAPE"), ("Toplam hata", "total_error_pct")],
)

# Hotel output generated by the final SARIMA.ipynb hotel cell already contains SARIMAX + corrections.
hotel_predictions = pd.read_csv(OUTPUT_DIR / "top20_2026_jan_jul_sarimax_may_june_predictions.csv")
hotel_scores = pd.read_csv(OUTPUT_DIR / "top20_2026_jan_jul_sarimax_may_june_model_scores.csv")
hotel_predictions["month"] = pd.to_datetime(hotel_predictions["month"])
selected_scores = hotel_scores.loc[hotel_scores["selected"].astype(str).str.lower().eq("true")].copy()
selected_scores = selected_scores.rename(columns={"season_total_absolute_error_pct": "total_error_pct"})
selected_scores.to_csv(OUTPUT_DIR / "sunum1_2026_hotel_sarimax_adjusted_scores.csv", index=False)
selected_hotels = selected_scores.sort_values("WMAPE").head(20)[["hotel_id", "hotel_name", "model", "WMAPE", "total_error_pct", "R2"]]
hotel_predictions = hotel_predictions.merge(selected_hotels[["hotel_id", "total_error_pct", "WMAPE", "R2"]], on="hotel_id", how="inner")
# The source predictions have separate baseline/adjusted columns; use the selected model flag.
hotel_predictions["prediction"] = hotel_predictions["selected_prediction"]
hotel_predictions.to_csv(OUTPUT_DIR / "sunum1_2026_hotel_sarimax_adjusted_predictions.csv", index=False)
save_clean_panels(
    hotel_predictions,
    "hotel_name",
    "prediction",
    "Antalya Otel Bazlı 2026 Backtest: SARIMAX + Takvim Düzeltmesi",
    "sunum1_2026_hotel_sarimax_adjusted_clean.png",
    [("WMAPE", "WMAPE"), ("Toplam hata", "total_error_pct")],
)
print("Clean SARIMAX revision outputs written.")
