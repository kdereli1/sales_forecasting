# Antalya ve Muğla Inhouse Analizi ve Tahminleme

## 1. Yönetici Özeti

Bu çalışma, Antalya ve Muğla'daki otellerin **inhouse** performansını geçmiş veriler üzerinden analiz etmek, sezon etkisini görünür kılmak ve 2026 gerçekleşenleriyle tahmin yaklaşımını sınamak için hazırlandı.

Odak noktaları:

- Antalya geneli için aylık inhouse serisi, sezon etkisi ve 2026 test tahminini değerlendirmek.
- Antalya'da otel ve ilçe/bölge seviyesinde satış hacmi, sezon ve tahmin performansını karşılaştırmak.
- Muğla'da 2026 Ocak-Temmuz inhouse hacmine göre öne çıkan otelleri belirlemek.
- 2022-2025 verisiyle eğitilen modellerin 2026 gerçekleşenlerine yakınlığını ölçmek.
- Muğla'nın en tutarlı 12 oteli için ayrıntılı model değerlendirmesi, ilk 50 otel için hacim ve sezon eğrileri sunmak.

## 2. Veri Seti

Kaynak dosya: `data/complete_cleaned_data_full.csv`

| Başlık | Bilgi |
|---|---|
| Kayıt sayısı | 343.060 rezervasyon kaydı |
| Kolon sayısı | 18 |
| Analiz seviyesi | Rezervasyon, otel, otel bölgesi, giriş/çıkış tarihi |
| Ana metrik | Inhouse: konaklanan gecelerin toplamı |
| Şehir odağı | Antalya ve Muğla |
| Tarih kapsamı | 2022-01-01 ile 2026-07-31 |

Temel alanlar: `sehir_adi`, `hotel_id`, `hotel_name`, `hotel_region_name`, `voucher_checkin_date`, `voucher_checout_date`, kişi ve oda bilgileri.

## 3. Veriyi Nasıl Hazırladık?

1. Antalya ve Muğla rezervasyonları şehir alanı ile ayrıştırıldı.
2. Giriş ve çıkış tarihleri doğrulandı; geçersiz veya sıfır gecelik kayıtlar dışarıda bırakıldı.
3. Her rezervasyon, kaldığı gecelere açıldı. Böylece sadece rezervasyon adedi değil, gerçek **occupied nights / inhouse** ölçüldü.
4. Günlük geceler otel ve ay seviyesinde toplulaştırıldı.
5. Eksik aylara `0` inhouse atanarak kesintisiz aylık seriler oluşturuldu.

Bu yaklaşım, check-in ayına göre basit rezervasyon sayımı yerine konaklamanın gerçekleştiği tarihe göre gerçek inhouse hacmini ölçer.

## 4. Antalya Analizi

### Antalya geneli

Antalya için tüm otellerin geceleri aylık seriye dönüştürüldü. SARIMAX ve Prophet karşılaştırıldı; takvim kaymasının etkisini görmek için Mayıs tatil düzeltmesi ve Haziran talep transferi ile birlikte ele alındı. 2026 Ocak-Temmuz gerçekleşenleri test dönemi olarak kullanıldı.

- Aylık inhouse zaman serisi: `OUTPUT_SARIMA/monthly_time_series.png`
- Yıllara göre mevsim eğrileri: `OUTPUT_SARIMA/seasonal_curves.png`
- 2026 gerçek ve tahmin karşılaştırması: `OUTPUT_SARIMA/test_predictions_comparison.png`
- Model karşılaştırması: `OUTPUT_SARIMA/model_comparison.csv`
- 2027 ileri tahmin: `OUTPUT_SARIMA/forecast_2027.csv`

### Antalya otelleri

2026 Ocak-Temmuz inhouse hacmiyle seçilen ilk 20 Antalya oteli için aylık gerçek/tahmin grafikleri, model skorları ve yıllık karşılaştırmalar üretildi. Ek sezonsal çalışmada ilk 30 otel ile sezon/sezon dışı görünüm ayrıca değerlendirildi.

- İlk 20 otel, gerçek ve en iyi model: `OUTPUT_SARIMA/top20_2026_actual_vs_best_model_with_metrics.png`
- İlk 20 otel aylık yoğunluk haritası: `OUTPUT_SARIMA/top20_hotels_monthly_inhouse_heatmap.png`
- İlk 20 otel skorları: `OUTPUT_SARIMA/top20_2026_hotel_model_scores.csv`
- Sezon kalitesi sıralaması: `OUTPUT_SARIMA/top26_seasonal_ranking_best_to_worst.csv`

### Antalya ilçe/bölgeleri

Veride resmi ilçe alanı olmadığı için Antalya otel bölgeleri önce ilçe vekili olarak ele alındı; ayrıca bölge-ilçe eşlemesi ile resmi ilçe düzeyinde sezon ve sezon dışı toplamları üretildi. İlçe tahminlerinde SARIMAX ve Prophet karşılaştırıldı; 2026 Mart-Temmuz için ayrıca Ridge tabanlı aylık backtest uygulandı.

- Aktif ilçe/bölge model panelleri: `OUTPUT_SARIMA/active_district_2025_actual_vs_model_metrics.png`
- 2026 Mart-Temmuz ilçe backtest grafiği: `OUTPUT_SARIMA/district_monthly_mar_jul_2026_actual_vs_prediction.png`
- İlçe toplam mutlak hata sıralaması: `OUTPUT_SARIMA/district_monthly_mar_jul_2026_total_error_ranking.png`
- İlçe MAPE, WMAPE ve R2 özeti: `OUTPUT_SARIMA/district_monthly_mar_jul_2026_mape_wmape_r2_summary.csv`

## 5. Sezon Tanımı

| Dönem | Aylar |
|---|---|
| Sezon | Mart - Ekim |
| Sezon dışı | Kasım - Şubat |
| 2026 mevcut sezon verisi | Mart - Temmuz |
| 2026 mevcut sezon dışı verisi | Ocak - Şubat |

2026 verisi Temmuz sonunda bittiği için 2026 sezon değeri tam sezon değil, **Mart-Temmuz gerçekleşeni** olarak yorumlanmalıdır.

## 6. Muğla Otel Seçim Mantığı

### İlk 50 otel

Muğla'da 2026 Ocak-Temmuz toplam inhouse değerine göre en yüksek hacimli 50 otel seçildi. Bu grup, ticari açıdan en yüksek satış hacmine sahip otellerin sezon ve aylık davranışını karşılaştırmak için kullanılır.

Çıktı: `outputs/OUTPUT_SARIMA/mugla_top50_hotels_by_2026_jan_july_inhouse.csv`

### Ayrıntılı 12 otel

Modelleme için daha güvenilir zaman serileri elde etmek amacıyla önce 2026 Ocak-Temmuz inhouse'a göre ilk 30 otel belirlendi. Ardından bir otelin seçilebilmesi için 2022, 2023, 2024 ve 2025 yıllarının her birinde Mart-Ekim sezon toplamının en az 100 inhouse olması istendi.

Bu filtre ile 12 otel kaldı. Bu grup, geçmişte düzenli satış sinyali taşıdığı için tahminleme değerlendirmesinde kullanıldı.

Çıktı: `outputs/OUTPUT_SARIMA/mugla_12_eligible_hotels_by_2026_jan_july_inhouse.csv`

## 7. Muğla Tahminleme Yaklaşımı

### Eğitim ve test tasarımı

| Aşama | Tarih aralığı |
|---|---|
| Eğitim | 2022-01 - 2025-12 |
| Backtest | 2026-01 - 2026-07 |
| Ana model seçimi | 2026 Mart-Temmuz |

Her otel için iki aday test edildi:

1. **SARIMAX baseline**
2. **SARIMAX + Mayıs uplift + Haziran transferi**

Mayıs düzeltmesi ve Haziran transfer katsayısı yalnızca eğitim döneminden, yani 2022-2025 verisinden türetildi. Böylece 2026 test gerçekleşenleri ile model parametresi belirlenmedi; veri sızıntısı engellendi.

## 8. Model Seçim Kriterleri

Birincil seçim metriği **WMAPE**, eşitlik bozucu ise **MAE** oldu.

$$
\mathrm{WMAPE} = \frac{\sum |\mathrm{gercek} - \mathrm{tahmin}|}{\sum |\mathrm{gercek}|} \times 100
$$

Sezon ve sezon dışı toplamlar için ayrıca aşağıdaki iş metriği raporlandı:

$$
\mathrm{Toplam\ Mutlak\ Hata\ Orani} =
\frac{|\mathrm{tahmin\ toplam\ inhouse} - \mathrm{gercek\ toplam\ inhouse}|}{\mathrm{gercek\ toplam\ inhouse}} \times 100
$$

Gerçek toplam inhouse sıfırsa yüzde oranı hesaplanmaz ve `NaN` olarak tutulur.

## 9. Sunumda Kullanılacak Görseller

### Filtrelenmiş 12 otel

- Sezon ve sezon dışı yıllık çizgiler: `outputs/OUTPUT_SARIMA/mugla_12_hotels_season_offseason_2022_2026_lines.png`
- 2022-2026 Ocak-Temmuz yılları üst üste çizgiler: `outputs/OUTPUT_SARIMA/mugla_12_hotels_jan_jul_2022_2026_overlay_lines.png`
- 2026 backtest, tahmin ve metrik panelleri: `outputs/OUTPUT_SARIMA/mugla_12_2026_jan_jul_sarimax_may_june_backtest_metrics.png`

### 2026 hacmine göre ilk 50 otel

- Sezon ve sezon dışı yıllık çizgiler: `outputs/OUTPUT_SARIMA/mugla_top50_hotels_season_offseason_2022_2026_lines.png`
- 2022-2026 Ocak-Temmuz yılları üst üste çizgiler: `outputs/OUTPUT_SARIMA/mugla_top50_hotels_jan_jul_2022_2026_overlay_lines.png`

## 10. Ana Mesajlar

- Inhouse performansı, yalnızca toplam satıştan değil, konaklamanın hangi ayda gerçekleştiğinden etkilenir.
- Antalya analizi şehir geneli, otel ve ilçe/bölge seviyesinde karar desteği sağlar; Muğla analizi otel bazında daha ayrıntılı karşılaştırma sunar.
- Sezon hareketi otelden otele anlamlı biçimde değişir; bu nedenle tek bir Muğla geneli eğrisi ticari karar için yeterli değildir.
- Hacmi yüksek ilk 50 otel, ticari kapsama öncelik verir. Filtrelenmiş 12 otel ise daha uzun ve düzenli geçmişi sayesinde daha güvenilir model değerlendirmesi sağlar.
- Tahmin kalitesi aylık hata ile birlikte sezon toplamı ve sezon dışı toplamı açısından da izlenmelidir.
- 2026 yılı henüz tam yıl olmadığı için yıl bazlı karşılaştırmalarda Ocak-Temmuz ve Mart-Temmuz kapsamı açıkça belirtilmelidir.

## 11. Önerilen Sunum Akışı

1. İş hedefi ve neden inhouse ölçtüğümüz
2. Veri kaynağı, kapsam ve veri kalitesi yaklaşımı
3. Rezervasyon verisini gece bazlı inhouse serisine dönüştürme
4. Antalya geneli: aylık seri ve 2026 model performansı
5. Antalya otelleri: ilk 20 ve sezon karşılaştırması
6. Antalya ilçe/bölgeleri: performans ve hata sıralaması
7. Muğla: 2026 ilk 50 otelin hacim ve sezon görünümü
8. Muğla: filtrelenmiş 12 otelin seçilme mantığı
9. Muğla: 12 otelin sezon ve Ocak-Temmuz karşılaştırması
10. SARIMAX backtest yaklaşımı ve metrikler
11. Sonuçlar, kullanım alanları ve sonraki adımlar

## 12. Sonraki Adımlar

- 2026 Ağustos-Aralık gerçekleşenleri geldikçe backtest penceresini güncellemek.
- Otel segmenti, oda kapasitesi, kaynak pazar ve fiyat bilgisi eklenebiliyorsa modele dışsal değişken olarak değerlendirmek.
- Mayıs tatil etkisi ve Haziran talep transferini resmi tatil/etkinlik takvimiyle güçlendirmek.
- İlk 50 otel için operasyonel eşikler belirlemek: yüksek hacim, yüksek büyüme, yüksek tahmin hatası ve sezon dışı fırsat listeleri.

## Ek: Çıktı Dosyaları

### Antalya

- Antalya model özeti: `OUTPUT_SARIMA/model_selection_summary.csv`
- Antalya aylık gerçekleşenler: `OUTPUT_SARIMA/antalya_monthly_occupied_nights.csv`
- Antalya ilçe sezon/sezon dışı tablosu: `OUTPUT_SARIMA/all_official_antalya_districts_season_offseason_inhouse_2023_2025_wide.csv`

- 12 otel model skorları: `outputs/OUTPUT_SARIMA/mugla_12_2026_mar_jul_sarimax_may_june_model_scores.csv`
- 12 otel WMAPE sıralaması: `outputs/OUTPUT_SARIMA/mugla_12_2026_mar_jul_selected_hotels_wmape_ranking.csv`
- 12 otel sezon / sezon dışı toplamları: `outputs/OUTPUT_SARIMA/mugla_12_2026_season_offseason_selected_total_error.csv`
- İlk 50 otel seçimi: `outputs/OUTPUT_SARIMA/mugla_top50_hotels_by_2026_jan_july_inhouse.csv`