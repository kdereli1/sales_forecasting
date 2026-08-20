# Antalya Cluster Bazlı Talep Tahmini - Özet Rapor

## 1. Seçilen optimum cluster sayısı

`k=2..8` aralığında silhouette, Davies-Bouldin ve inertia dirsek gücünün normalize birleşik skoru kullanıldı. Seçilen optimum cluster sayısı **4** oldu. Merkezler, 2025 toplam occupied nights değeri en az 30 olan 205 otelde öğrenildi; düşük sinyalli oteller en yakın merkeze atandı.

| k | silhouette | davies_bouldin | inertia | elbow_strength | selection_score |
| --- | --- | --- | --- | --- | --- |
| 2.0000 | 0.2049 | 1.8085 | 332.1122 | 0.0000 | 1.4140 |
| 3.0000 | 0.2005 | 1.6864 | 299.1740 | 0.1295 | 2.1026 |
| 4.0000 | 0.2046 | 1.5705 | 273.6392 | 0.1924 | 2.8074 |
| 5.0000 | 0.1823 | 2.0529 | 257.6154 | 0.1698 | 0.8826 |
| 6.0000 | 0.1847 | 1.8933 | 242.2959 | 0.1409 | 1.1094 |
| 7.0000 | 0.1970 | 1.4626 | 233.1218 | 0.0567 | 1.9477 |
| 8.0000 | 0.1858 | 1.5195 | 220.8963 | 0.0000 | 1.0586 |

## 2. Cluster özellikleri

| cluster_id | hotel_count | center_fit_hotel_count | total_sales | average_daily_sales | average_season_length | annual_total_2025 | peak_intensity | coefficient_of_variation | summer_winter_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.000 | 737.000 | 102.000 | 99564.000 | 0.092 | 0.970 | 10723.000 | 0.253 | 2.756 | 10.413 |
| 1.000 | 82.000 | 82.000 | 317889.000 | 2.653 | 4.329 | 110126.000 | 0.332 | 1.746 | 736.967 |
| 2.000 | 18.000 | 2.000 | 1270.000 | 0.048 | 2.278 | 301.000 | 0.669 | 10.073 | 0.522 |
| 3.000 | 30.000 | 19.000 | 28475.000 | 0.650 | 5.100 | 9445.000 | 0.418 | 4.840 | 9.957 |

Cluster merkezlerinin tam 365 günlük eğrileri `cluster_centers.csv`, otel atamaları `hotel_cluster_assignments.csv` dosyasındadır.

## 3. Her cluster için en iyi model

2025 Ocak-Temmuz recursive validation WMAPE sonucuna göre seçim yapıldı.

| cluster_id | otel_sayisi | secilen_model |
| --- | --- | --- |
| 0 | 737 | GradientBoosting |
| 1 | 82 | GradientBoosting |
| 2 | 18 | CatBoost |
| 3 | 30 | CatBoost |

## 4. Cluster bazlı hata metrikleri

| cluster_id | hotel_count | secilen_model | MAE | WMAE | RMSE | MAPE | WMAPE | R2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.000 | 737.000 | GradientBoosting | 0.075 | 5.810 | 0.610 | 94.440 | 123.871 | -0.039 |
| 1.000 | 82.000 | GradientBoosting | 2.991 | 23.618 | 8.452 | 90.551 | 88.043 | 0.146 |
| 2.000 | 18.000 | CatBoost | 0.023 | 1.326 | 0.173 | 100.000 | 100.000 | -0.017 |
| 3.000 | 30.000 | CatBoost | 1.018 | 11.655 | 3.435 | 99.192 | 99.820 | -0.077 |

Tüm Antalya testinde MAE **0.383**, RMSE **2.735**, WMAPE **93.61%** ve R² **0.218** oldu.

## 5. En yüksek hacimli otellerin performansı

İlk 10 görünümü aşağıdadır; tam ilk 20 liste `top20_volume_hotels.csv` dosyasındadır.

| hotel_id | hotel_name | cluster | model | actual_total | predicted_total | WMAPE | R2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 456.00 | Robinson Çamyuva | 1.00 | GradientBoosting | 3190.00 | 342.71 | 90.16 | -0.10 |
| 181147.00 | Belek Beach Resort Hotel | 1.00 | GradientBoosting | 2936.00 | 338.98 | 88.64 | -0.20 |
| 201949.00 | Monachus Family Resort Sorgun | 1.00 | GradientBoosting | 2656.00 | 342.71 | 87.42 | -0.10 |
| 887.00 | Sueno Hotels Deluxe Belek | 1.00 | GradientBoosting | 2253.00 | 454.42 | 85.97 | -0.11 |
| 813.00 | Champion Holiday Village | 1.00 | GradientBoosting | 2228.00 | 342.70 | 89.18 | -0.01 |
| 471.00 | Crystal Admiral Aqua Collection | 1.00 | GradientBoosting | 1975.00 | 342.74 | 86.20 | -0.02 |
| 1266.00 | Swandor Hotels & Resort Topkapı Palace | 3.00 | CatBoost | 1917.00 | 23.19 | 99.06 | -0.62 |
| 646.00 | Crystal Waterworld Aqua Collection | 1.00 | GradientBoosting | 1897.00 | 349.63 | 83.52 | -0.04 |
| 181836.00 | La Benata Hotel | 1.00 | GradientBoosting | 1890.00 | 342.60 | 86.43 | -0.01 |
| 647.00 | Crystal Sunset Pearl Collection | 1.00 | GradientBoosting | 1868.00 | 342.69 | 81.99 | 0.00 |

## 6. En başarılı otellerin performansı

WMAPE sıralamasında gerçek toplamı sıfır olan oteller dışarıda bırakıldı. İlk 10 görünümü aşağıdadır; tam ilk 20 liste `best_accuracy_hotels.csv` dosyasındadır.

| hotel_id | hotel_name | cluster | model | MAE | WMAPE | R2 |
| --- | --- | --- | --- | --- | --- | --- |
| 9933.00 | Paloma Finesse | 1.00 | GradientBoosting | 1.09 | 56.39 | 0.54 |
| 3213.00 | Club Marco Polo | 1.00 | GradientBoosting | 1.50 | 56.72 | 0.47 |
| 168642.00 | Rubi Platinum Sign | 1.00 | GradientBoosting | 1.21 | 60.41 | 0.51 |
| 1400.00 | Orange County Alanya | 1.00 | GradientBoosting | 2.22 | 60.47 | 0.35 |
| 9621.00 | Kirman Belazur Resort & Spa | 1.00 | GradientBoosting | 1.08 | 62.20 | 0.51 |
| 3106.00 | Leodikya Kirman Premium | 1.00 | GradientBoosting | 1.07 | 62.25 | 0.59 |
| 886.00 | Kimeros Park Holiday Village | 1.00 | GradientBoosting | 2.47 | 64.33 | 0.35 |
| 698.00 | Aydınbey Gold Dreams Hotel | 1.00 | GradientBoosting | 0.97 | 64.76 | 0.42 |
| 468.00 | Sueno Hotels Golf Belek | 1.00 | GradientBoosting | 1.74 | 65.00 | 0.28 |
| 275208.00 | Paloma Sencia | 1.00 | GradientBoosting | 2.11 | 65.33 | 0.42 |

## 7. Antalya toplam aylık performansı

| Ay | Gercek | Tahmin | Fark | Yuzde_Hata |
| --- | --- | --- | --- | --- |
| 2026-01 | 1436.00 | 442.01 | -993.99 | 69.22 |
| 2026-02 | 298.00 | 465.61 | 167.61 | 56.24 |
| 2026-03 | 1846.00 | 655.02 | -1190.98 | 64.52 |
| 2026-04 | 1441.00 | 1170.23 | -270.77 | 18.79 |
| 2026-05 | 14822.00 | 3503.81 | -11318.19 | 76.36 |
| 2026-06 | 12702.00 | 9339.50 | -3362.50 | 26.47 |
| 2026-07 | 42613.00 | 16750.55 | -25862.45 | 60.69 |

Ocak-Temmuz gerçek toplamı **75,158**, tahmin toplamı **32,327** occupied nights oldu. Toplam yanlılık **-56.99%**. En düşük aylık yüzde hata **2026-04 (18.79%)**, en yüksek hata **2026-05 (76.36%)** döneminde görüldü.

## 8. Güçlü ve zayıf yönler

**Güçlü yönler**

- Check-in dahil/check-out hariç gerçek inhouse hedefi ve kesintisiz otel-gün paneli kullanıldı.
- Cluster seçimi birden çok iç kalite metriğine, model seçimi ileri dönem recursive validation'a dayandırıldı.
- Cluster bazında farklı algoritma seçimine ve otel/cluster/Antalya seviyesinde izlenebilir çıktılara izin verildi.

**Zayıf yönler**

- 2026 yaz hacmi ciddi biçimde düşük tahmin edildi; toplam yanlılık -56.99% ve genel WMAPE 93.61% seviyesinde.
- Cluster 0 çok sayıda düşük sinyalli otel içeriyor; sparse serilerde oran metrikleri ve recursive tahmin kararsızlaşabiliyor.
- İstenen feature setinde otel kimliği, kapasite, fiyat, pazar, rezervasyon eğrisi veya tatil/event bilgisi yok. Pooled cluster modeli aynı takvim/lag durumundaki otelleri ayırt edemiyor.
- Recursive yaklaşım uzun ufukta hatayı biriktiriyor. Validation sonuçlarındaki bazı ağaç modellerinin aşırı WMAPE değerleri bu riski gösteriyor.

## 9. Gelecek sezon kullanım önerileri

1. Bu sürümü doğrudan operasyonel bütçe tahmini olarak kullanmayın; özellikle Mayıs-Temmuz için kalibrasyon ve insan kontrolü uygulayın.
2. Otel kapasitesi ve otel kimliği/embedding, fiyat, bölge, konsept, pazar ve resmi tatil-event feature'larını ekleyin.
3. Düşük hacimli otelleri ayrı bir zero-inflated veya occurrence-plus-volume modeliyle ele alın; minimum geçmiş/hacim eşiği tanımlayın.
4. Tek seferlik 7 aylık recursive tahmin yerine haftalık/aylık yeniden tahmin ve expanding-window backtest kullanın.
5. Model seçimini yalnız WMAPE değil WMAPE, bias ve R² birlikte izleyen iş kuralıyla yapın; yaz aylarına daha yüksek ağırlık verin.
6. 2026 verisinin henüz tamamlanmamış veya booking cut-off etkisi taşıyıp taşımadığını doğrulayın; kaynak kapsamı eksikse hata modelden değil veri olgunluğundan kaynaklanabilir.
