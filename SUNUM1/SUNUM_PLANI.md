# SUNUM1 — Antalya & Muğla Talep Analizi · Sunum Planı

**Kaynak:** `notebooks/SARIMA.ipynb` (defterin kendi kayıtlı çıktıları)
**Sunum:** `Antalya_Mugla_Talep_Analizi_SUNUM1.pptx` — 38 slayt, 23 gömülü görsel
**Görseller:** `gorseller/` — defterden çıkarılan 57 grafik
**Tarih:** 26 Ağustos 2026

> Her slaytta **konuşmacı notu** var. PowerPoint'te `Görünüm → Notlar`, sunum sırasında
> `Sunum Görünümü` ile okuyabilirsiniz.

---

## 1. Bir Cümlelik Mesaj

> Antalya ve Muğla'da aylık konaklama talebini şehir, ilçe ve otel kırılımında modelledik;
> her iki şehirde de **bayram takvimi düzeltmesi hatayı yarı yarıya azalttı** (Antalya %37→%17,6,
> Muğla %28→%19,5), ancak bu rakamların nasıl okunması gerektiğine dair iki metodolojik uyarı var.

---

## 2. Anahtar Sayılar

### Şehir seviyesi · 2026 Ocak-Temmuz backtest

| Model | Antalya MAE | Antalya WMAPE | Antalya R² | Muğla MAE | Muğla WMAPE | Muğla R² |
|---|---|---|---|---|---|---|
| SARIMAX + takvim düzeltmesi | 1.892 | **%17,6** | 0,975 | 790 | **%19,5** | 0,916 |
| Prophet + takvim düzeltmesi | 2.486 | %23,2 | 0,938 | 976 | %24,1 | 0,928 |
| SARIMAX baseline | 3.968 | %37,0 | 0,850 | 1.143 | %28,2 | 0,888 |
| Prophet baseline | 4.529 | %42,2 | 0,792 | 1.176 | %29,1 | 0,912 |

**Takvim düzeltme katsayıları**
- Antalya: Haziran transfer faktörü **0,648** (talep Mayıs'a çekildi, Haziran çöktü)
- Muğla: Mayıs uplift **+2.467 gece**, Haziran transfer **1,000** (Haziran düşmedi)

### Antalya ilçeleri · 2025 backtest (eğitim 2023-2024)

| İlçe | Model | WMAPE % | Sezon hata % | R² |
|---|---|---|---|---|
| Kemer | SARIMAX | 22,3 | **8,4** | 0,95 |
| Kumluca | Prophet | 32,7 | 8,8 | 0,88 |
| Serik | SARIMAX | 31,5 | 9,1 | 0,88 |
| Muratpaşa | SARIMAX | 30,4 | 14,0 | 0,70 |
| Alanya | SARIMAX | 27,1 | 22,5 | 0,91 |
| Manavgat | Prophet | 27,4 | 23,2 | 0,86 |
| Kaş | Prophet | 38,4 | 35,3 | 0,79 |

Dışlanan düşük hacimli ilçeler: Aksu, Döşemealtı, Finike, Kepez, Konyaaltı

### Antalya ilçeleri · 2026 Mart-Temmuz (Ridge, takvim düzeltmesiz)

Kumluca %26,2 · Muratpaşa %51,0 · Alanya %53,0 · Serik %60,5 · Kaş %61,6 · Manavgat %64,1 · Kemer %66,6

> Bu tablo takvim düzeltmesinin değerini dolaylı kanıtlar: düzeltme uygulanmayan model aynı dönemde çok daha kötü.

### Muğla ilçeleri · 2026 Ocak-Temmuz backtest

| İlçe | Model | WMAPE % | Sezon toplam hata % | R² |
|---|---|---|---|---|
| Datça | SARIMAX_adj | **15,2** | 4,2 | 0,99 |
| Fethiye | Prophet_adj | 16,3 | 4,6 | 0,97 |
| Ortaca | SARIMAX_adj | 23,7 | **0,8** | 0,94 |
| Bodrum | SARIMAX_adj | 27,2 | 21,0 | 0,84 |
| Ula | Prophet_adj | 28,2 | 7,2 | 0,89 |
| Milas | SARIMAX_adj | 85,2 | 32,6 | 0,04 |
| **Marmaris** | SARIMAX_adj | **201,1** | 192,3 | **−10,8** |

### Oteller

**Antalya (Top 20, 2026 Oca-Tem):** Sueno Deluxe Belek %31,9 (Prophet) · Robinson Çamyuva %32,5 (SARIMAX) ·
Belek Beach %36,3 · Crystal Admiral %44,8 · Champion Holiday Village %70,1

**Muğla (filtreli 12, Mar-Tem 2026):** Divan Bodrum %18,8 · Costa Farilya %23,8 ·
Golden Age Yalıkavak %35,6 · Manaspark %37,1 · Robinson Sarıgerme %50,6 *(ama sezon toplam hatası sadece %2,7)*

---

## 3. İki Metodolojik Uyarı (34. ve 35. slaytlar)

### Uyarı 1 — Kalibrasyon sızıntısı
Takvim düzeltme katsayıları test döneminin **gerçek değerlerinden** hesaplanıyor:

```
holiday_uplift       = may_actual - base_sarimax_test.loc[may_2026]   # 2026 Mayıs GERÇEĞİ
june_transfer_factor = june_2026_actual / june_historical_mean        # 2026 Haziran GERÇEĞİ
```

Dolayısıyla **%17,6 kör bir tahmin başarısı değildir.** Doğru okunuşu:
*"Bayram kaymasını bildiğimizi varsayarsak kalan hata %17,6'dır."*
Gerçek out-of-sample performans baseline rakamlarıdır: Antalya %37,0, Muğla %28,2.

**Sunumda nasıl söylenmeli:** "Düzeltmesiz %37 → takvim etkisini modellediğimizde %17,6'ya iniyor."

### Uyarı 2 — SARIMAX uzun ufukta negatif üretiyor
Defter çıktısı: **2027 Haziran tahmini −48.037 gece.** Occupied nights negatif olamaz.
Kök neden: `order=(1,2,1)` ikinci derece farklanma + sabit trend terimi.
Uygulanan yama: 2027 için Prophet baseline'a geçildi, takvim düzeltmeleri üzerine eklendi.
Kalıcı çözüm: `trend='n'` veya log dönüşümü, tahmin ufkunu 6 aya indirme, rolling refit.

---

## 4. Slayt Akışı ve Süre Planı (~30 dk sunum + 10 dk soru)

| # | Slayt | Süre | Ana mesaj |
|---|---|---|---|
| 1 | Kapak | 0:30 | Amaç ve kapsam |
| 2 | Yönetici Özeti | 2:00 | 4 KPI + iki uyarının önceden duyurulması |
| 3 | Veri ve Kapsam | 1:30 | occupied nights tanımı, kırılımlar, hacim filtreleri |
| 4 | Metodoloji | 2:00 | SARIMAX + Prophet + takvim düzeltmesi + birim bazlı seçim |
| 5 | Metrikler | 2:00 | WMAPE vs toplam hata — **tartışmayı yöneten slayt** |
| **6** | **BÖLÜM 1 · ANTALYA** | — | Geçiş |
| 7 | Antalya aylık seri | 1:00 | Düzenli, yüksek hacimli, net mevsimsellik |
| 8 | **Yıl bazlı mevsimsel eğriler** | 2:00 | 2026'nın diğer yıllardan ayrıştığı yer — **kilit görsel** |
| 9 | Trend/mevsimsellik ayrıştırma | 0:45 | Seri trend + mevsimsellik ile açıklanıyor |
| 10 | **Takvim etkisi ve düzeltme** | 2:30 | %36,95 → %17,62 — **sunumun kalbi** |
| 11 | Antalya 2026 backtest | 1:30 | 4 model tablosu + grafik |
| 12 | Aylık hata dağılımı | 0:45 | Model yanlı değil |
| 13 | İlçe sezon/sezon dışı hacim | 1:00 | Hacim dağılımı |
| 14 | İlçe 2025 backtest panelleri | 1:30 | Her ilçe kendi modeliyle |
| 15 | İlçe kalite sıralaması | 1:30 | Kemer en iyi, model dağılımı karışık |
| 16 | Seçili 7 ilçe aylık | 1:00 | Karar için en anlamlı kırılım |
| 17 | İlçe 2026 Mar-Tem (Ridge) | 1:30 | Düzeltmesiz model neden kötü |
| 18 | Otel ısı haritası | 0:45 | Otel doluluk profilleri |
| 19 | Otel yıl bazlı hacim | 0:45 | Büyüyen/daralan oteller |
| 20 | Otel 2026 backtest | 1:30 | En iyi %32, %60 üzeri kullanılmaz |
| 21 | Otel sezon/sezon dışı | 0:45 | Antalya'nın sezon dışı satışı var |
| **22** | **BÖLÜM 2 · MUĞLA** | — | Geçiş |
| 23 | Muğla mevsimsel eğriler | 1:00 | Daha keskin mevsimsellik |
| 24 | Muğla sezon/sezon dışı | 0:45 | Sezon dışı neredeyse sıfır |
| 25 | Muğla 2026 backtest | 1:30 | %19,5 + Haziran transferi 1,000 bulgusu |
| 26 | Muğla ilçe hacim | 1:00 | Bodrum baskınlığı |
| 27 | Muğla ilçe 55 aylık trend | 1:00 | Marmaris düşüşü burada görülüyor |
| 28 | Muğla ilçe backtest | 1:30 | Datça/Fethiye çok iyi, **Marmaris %201** |
| 29 | Muğla ilçe panelleri | 0:45 | Ortaca %0,8 toplam hata |
| 30 | Muğla otel backtest | 1:30 | Divan Bodrum %18,8; Robinson metrik paradoksu |
| 31 | Muğla otel sezon trendi | 0:45 | Sezon dışı sıfıra yakın |
| 32 | **Antalya vs Muğla karşılaştırma** | 2:00 | Ortalama mı, uç değer mi? |
| 33 | **Neden bu farklar?** | 2:00 | Hacim, dağılım, sezon uzunluğu, bayram tepkisi |
| 34 | **Uyarı 1 · Sızıntı** | 2:00 | %17,6 nasıl okunmalı — **atlanmamalı** |
| 35 | **Uyarı 2 · Negatif tahmin** | 1:30 | 2027 Haziran −48.037 |
| 36 | Riskler ve sınırlar | 1:30 | Dürüst değerlendirme |
| 37 | Öneriler | 1:30 | Somut aksiyonlar |
| 38 | Kapanış | — | Q&A |

**Kısaltmak gerekirse çıkarılabilecek slaytlar:** 9, 12, 18, 19, 21, 29, 31 (≈5 dk kazanç)

---

## 5. Anlatım Kurgusu

1. **Kur** (1-5): Ne yaptık, hangi veriyle, hangi metrikle bakacağız.
2. **Antalya'yı tanı** (6-9): Talep karakteri, mevsimsellik.
3. **Sürprizi açıkla** (10): 2026 neden şaştı → bayram kayması. *Burada durun.*
4. **Antalya sonuçları** (11-21): Şehir → ilçe → otel, kademeli derinleşme.
5. **Muğla'yı tanı ve sonuçları** (22-31): Aynı akış, farklı karakter.
6. **Karşılaştır ve sebeplendir** (32-33): İki şehir neden farklı davranıyor.
7. **Kendini sorgula** (34-36): İki metodolojik uyarı + riskler.
8. **Kapat** (37-38): Aksiyon planı, Q&A.

---

## 6. Antalya ve Muğla Neden Farklı?

| Faktör | Antalya | Muğla | Modele etkisi |
|---|---|---|---|
| Rezervasyon hacmi | ~2,5 kat büyük | Daha küçük | Yüksek hacim → düşük oransal gürültü |
| Talep dağılımı | 12 ilçeye yayılmış | Bodrum baskın | Konsantrasyon → tek kırılma toplamı bozar |
| Sezon dışı satış | Var (Ocak ~1.000 gece) | Neredeyse yok (Ocak ~30) | Sıfıra yakın aylar yüzdesel metrikleri patlatır |
| Bayram tepkisi | Haziran çöktü (faktör 0,648) | Haziran düşmedi (faktör 1,000) | Ayrı kalibrasyon gerekli |
| Sonuç varyansı | Dar bant (%22-38) | Geniş bant (%15-201) | Antalya'da genel güven, Muğla'da birim seçimi |

**Kilit cümle:** *"Fark modelden değil, veri karakterinden geliyor."*

---

## 7. Hazır Soru-Cevaplar

**S: %17,6 hata çok mu iyi, nasıl elde ettiniz?**
C: Takvim düzeltmesi test dönemi gerçeğinden kalibre edildi, bu yüzden kör tahmin başarısı değil.
Kör performans %37. 34. slaytta açıkça yazıyor.

**S: Neden bazı yerde SARIMAX, bazı yerde Prophet?**
C: Her ilçe/otel için ikisini de denedik, en düşük WMAPE'liyi otomatik seçtik. Tek model
dayatmak yerine birim bazında ölçüm yaptık.

**S: Marmaris'e ne oldu?**
C: 2026'da yapısal talep düşüşü yaşandı. Zaman serisi modelleri geçmişte örneği olmayan
kırılmaları öngöremez. R² −10,8 → bu birim için model kullanılmamalı.

**S: Antalya mı Muğla mı daha iyi tahmin ediliyor?**
C: Ortalamada Antalya (daha dengeli). Ama Muğla'nın en iyi birimleri Antalya'nınkinden daha iyi
(Datça %15, Divan Bodrum %19). Muğla'da varyans yüksek.

**S: Robinson Sarıgerme WMAPE %50 ama sezon hatası %2,7 — nasıl?**
C: Aylık dağılım şaşmış ama toplam tutmuş; fazla ve eksik tahminler birbirini götürmüş.
Kontenjan planlaması için toplam hata daha anlamlı. 5. slayta bakın.

**S: 2027 tahminini kullanabilir miyiz?**
C: Dikkatle. SARIMAX negatif ürettiği için Prophet yaması kullanıldı. Sezon dışı aylar
geçmiş ortalamayla kıyaslanmadan yayınlanmamalı. 35. slaytta detay var.

**S: Neden Prophet'i tamamen bırakmadınız?**
C: Bırakmadık çünkü bazı ilçe/otelde Prophet kazanıyor (Kumluca, Manavgat, Kaş, Fethiye, Ula)
ve uzun ufukta pozitif kalıyor. İkisi birbirini tamamlıyor.

---

## 8. Sunum Öncesi Kontrol Listesi

- [ ] `Antalya_Mugla_Talep_Analizi_SUNUM1.pptx` açılıyor, 38 slayt görünüyor
- [ ] Yoğun panel görselleri okunabilir (14, 16, 17, 20, 28, 29, 30)
- [ ] Sunum Görünümünde konuşmacı notları görünüyor
- [ ] 5., 8., 10., 32., 33. ve 34. slaytlar ezberde
- [ ] Anahtar sayılar hazır: **37,0 → 17,6** (Antalya) ve **28,2 → 19,5** (Muğla)
- [ ] Yedek: `notebooks/SARIMA.ipynb` açık bir sekmede (ham çıktı sorusu gelirse)

---

## 9. Dosya Haritası

```
SUNUM1/
├── SUNUM_PLANI.md                             ← bu dosya
├── Antalya_Mugla_Talep_Analizi_SUNUM1.pptx    ← sunum (38 slayt, notlu)
├── build_sunum1.py                            ← sunumu yeniden üreten script
├── extract_from_notebook.py                   ← defterden görsel/çıktı çıkarıcı
├── notebook_text_outputs.txt                  ← defterin tüm metin çıktıları (referans)
├── gorsel_manifest.json                       ← görsel ↔ hücre eşlemesi
└── gorseller/                                 ← 57 grafik (23'ü sunumda gömülü)
```

**Sunumu yeniden üretmek için:**
```powershell
.venv\Scripts\python.exe SUNUM1\extract_from_notebook.py   # defter çıktıları değiştiyse
.venv\Scripts\python.exe SUNUM1\build_sunum1.py
```

### Sunumda kullanılmayan ama elinizde olan görseller
`gorseller/` klasöründe ayrıca şunlar var (soru gelirse ekranda açabilirsiniz):
- `01_monthly_boxplot.png` — aylık dağılım kutu grafiği
- `15_top20_2026_actual_vs_best_model.png` — otel seçimi öncesi hali
- `17_top30_season_vs_offseason_year_totals.png` — Top 30 otel yıl toplamları
- `19_top30_district_2025_actual_vs_model_metrics.png` — 30 bölge proxy paneli
- `20`, `21` — Top 26 otel sezonsal backtest ve sıralama
- `22`, `23` — tüm resmi Antalya ilçeleri ve YoY değişim
- `25` — aktif ilçelerin tamamı (filtresiz)
- `37` — Muğla 2025 segment tahmini
- `39` — Muğla sezon odaklı metrikler
- `43`, `47_*` — Muğla Top 30 otel ve otel bazlı 2025 sezon tahminleri (12 ayrı grafik)
- `50_cell50_img2..4` — Muğla otel Ocak-Temmuz eğrileri ve ilk 50 otel panelleri
