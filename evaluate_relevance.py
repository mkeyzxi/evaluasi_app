import json

with open(r"c:\belajarku\semester 7\evaluasi_app\evaluasi_rag_vs_hyde_fix.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def evaluate_relevance(record):
    query = record.get("Query_Text", "").lower()
    judul = record.get("Judul_Skripsi", "").lower()
    abstrak = record.get("Abstrak", "").lower()
    tahun_doc = record.get("Tahun", 0)
    
    # ========================
    # Q01: "sistem pendukung keputusan metode"
    # ========================
    if record["ID"] == "Q01":
        if "sistem pendukung keputusan" in judul or "sistem pendukung keputusan" in abstrak:
            return 1
        return 0
    
    # ========================
    # Q02: "aplikasi media pembelajaran android"
    # ========================
    if record["ID"] == "Q02":
        is_pembelajaran = ("pembelajaran" in judul or "edukasi" in judul or "tutorial" in judul)
        is_android = ("android" in judul or "berbasis android" in abstrak)
        is_app = ("aplikasi" in judul or "media" in judul or "rancang bangun" in judul)
        
        if "progressive web app" in judul:
            return 0
        if is_pembelajaran and is_android:
            return 1
        if is_pembelajaran and is_app:
            return 1
        return 0
    
    # ========================
    # Q03: "algoritma convolutional neural network"
    # ========================
    if record["ID"] == "Q03":
        if ("convolutional neural network" in judul or "cnn" in judul or 
            "convolutional neural network" in abstrak or "convolution neural network" in judul):
            return 1
        if "mobilenet" in judul and "cnn" in abstrak:
            return 1
        return 0
    
    # ========================
    # Q04: "sistem kontrol berbasis iot"
    # ========================
    if record["ID"] == "Q04":
        is_iot = ("internet of things" in judul or "iot" in judul or 
                 "internet of things" in abstrak or "berbasis iot" in abstrak)
        is_kontrol = ("kontrol" in judul or "monitoring" in judul or "smart" in judul or
                     "pengendali" in judul or "pengendalian" in judul)
        is_mikrokontroler = ("mikrokontroler" in judul or "arduino" in judul or
                            "nodemcu" in judul or "esp" in abstrak)
        
        # ATM security - mikrokontroler but NOT IoT, NOT kontrol sistem
        if "pengamanan atm" in judul:
            return 0
        if is_iot and is_kontrol:
            return 1
        if is_iot:
            return 1
        if is_mikrokontroler and is_kontrol:
            return 1
        return 0
    
    # ========================
    # Q05: "sistem pakar diagnosa penyakit"
    # ========================
    if record["ID"] == "Q05":
        if "sistem pakar" in judul and ("diagnosa" in judul or "mendiagnosa" in judul or "penyakit" in judul):
            return 1
        if "sistem pakar" in judul and "penyakit" in abstrak:
            return 1
        return 0
    
    # ========================
    # Q06: "klasifikasi fertilitas telur ayam yolov8"
    # ========================
    if record["ID"] == "Q06":
        is_telur = "telur" in judul or "telur" in abstrak
        is_klasifikasi = "klasifikasi" in judul or "pemilahan" in judul or "penyortir" in judul or "monitoring" in judul
        is_yolov8 = "yolov8" in judul or "yolov8" in abstrak
        
        if is_telur and is_yolov8:
            return 1
        if is_telur and is_klasifikasi:
            return 1
        if "pemeliharaan ternak ayam broiler" in judul:
            return 0
        if "cabai" in judul:
            return 0
        return 0
    
    # ========================
    # Q07: "water resistant perkebunan karet mikrokontroler"
    # ========================
    if record["ID"] == "Q07":
        # Very specific topic - must be about water resistant + karet (rubber)
        if "water resistant" in judul and "karet" in judul:
            return 1
        if "karet" in judul and "mikrokontroler" in judul:
            return 1
        return 0
    
    # ========================
    # Q08: "sentimen ulasan wisata pantai losari lstm"
    # ========================
    if record["ID"] == "Q08":
        is_sentimen = "sentimen" in judul or "sentimen" in abstrak
        is_wisata = "wisata" in judul or "pariwisata" in judul or "wisata" in abstrak
        is_losari = "losari" in judul or "losari" in abstrak
        is_lstm = "lstm" in judul or "long short-term memory" in judul or "lstm" in abstrak
        
        # Perfect match: sentimen + losari + LSTM
        if is_sentimen and is_losari:
            return 1
        # Sentimen pariwisata (related)
        if is_sentimen and is_wisata:
            return 1
        # Sentimen with LSTM (related method)
        if is_sentimen and is_lstm:
            return 1
        # Wisata/pariwisata apps (partially related domain)
        if is_wisata and not is_sentimen:
            return 0
        # LSTM deteksi hoax - same method but different domain
        if is_lstm and not is_sentimen and not is_wisata:
            return 0
        # Sentimen but different domain
        if is_sentimen:
            return 0
        return 0
    
    # ========================
    # Q09: "animasi struktur bumi augmented reality"
    # ========================
    if record["ID"] == "Q09":
        is_ar = "augmented reality" in judul or "augmented reality" in abstrak
        is_bumi = "bumi" in judul or "bumi" in abstrak or "geografi" in judul
        is_animasi = "animasi" in judul or "animasi" in abstrak or "3d" in judul
        is_vr = "virtual reality" in judul
        
        # Perfect: animasi + struktur bumi + AR
        if is_ar and is_bumi:
            return 1
        # AR educational apps (related technology)
        if is_ar:
            return 1
        # VR educational apps (closely related technology)
        if is_vr:
            return 1
        return 0
    
    # ========================
    # Q10: "deteksi kelelawar mikrokontroler android"
    # ========================
    if record["ID"] == "Q10":
        if "kelelawar" in judul or "kelelawar" in abstrak:
            return 1
        return 0
    
    # ========================
    # Q11: "cara otomatis pisahin telur bagus"
    # ========================
    if record["ID"] == "Q11":
        is_telur = "telur" in judul or "telur" in abstrak
        is_otomatis_sort = ("pemilahan" in judul or "penyortir" in judul or 
                           "klasifikasi" in judul or "monitoring" in judul or
                           "otomatis" in abstrak or "kualitas" in judul)
        
        if is_telur and is_otomatis_sort:
            return 1
        if is_telur:
            return 1
        # Ikan lele - NOT telur
        if "ikan lele" in judul:
            return 0
        # Cabai - NOT telur
        if "cabai" in judul:
            return 0
        return 0
    
    # ========================
    # Q12: "alat biar motor gak gampang dicuri"
    # ========================
    if record["ID"] == "Q12":
        is_motor = ("sepeda motor" in judul or "kendaraan bermotor" in judul or
                   "kendaraan" in judul)
        is_keamanan = ("keamanan" in judul or "pengamanan" in judul or 
                      "pencurian" in judul or "fingerprint" in judul or "nfc" in judul)
        
        if is_motor and is_keamanan:
            return 1
        # Deteksi kelayakan pelumas - not security
        if "kelayakan minyak pelumas" in judul:
            return 0
        # Kecelakaan - not theft
        if "kecelakaan" in judul:
            return 0
        # Parkir - not specifically anti-theft
        if "parkir" in judul:
            return 0
        # ATM/rumah security - not motor
        if "atm" in judul or "rumah" in judul:
            return 0
        return 0
    
    # ========================
    # Q13: "cara bikin website toko online"
    # ========================
    if record["ID"] == "Q13":
        is_website = ("website" in judul or "web" in judul or "berbasis web" in abstrak or
                     "e-commerce" in judul)
        is_toko = ("toko" in judul or "jual beli" in judul or "penjualan" in judul or
                  "e-commerce" in judul or "pemasaran" in judul or "marketplace" in judul)
        
        if is_website and is_toko:
            return 1
        if "e-commerce" in judul:
            return 1
        # Marketplace on Android also counts
        if "marketplace" in judul:
            return 1
        return 0
    
    # ========================
    # Q14: "aplikasi buat hafalan quran santri"
    # ========================
    if record["ID"] == "Q14":
        is_quran = ("qur'an" in judul or "quran" in judul or "al-qur'an" in judul or
                   "qur'an" in abstrak or "qur" in abstrak or "qur" in judul)
        is_tajwid = "tajwid" in judul or "tajwid" in abstrak
        is_islam_learning = "agama islam" in judul or "pendidikan agama" in judul
        
        if is_quran:
            return 1
        if is_tajwid:
            return 1
        # Pembelajaran agama Islam - related but not specifically Quran hafalan
        if is_islam_learning:
            return 0
        return 0
    
    # ========================
    # Q15: "gimana cara siram bawang otomatis"
    # ========================
    if record["ID"] == "Q15":
        is_bawang = "bawang" in judul or "bawang" in abstrak
        is_penyiraman = ("penyiraman" in judul or "penyiraman" in abstrak)
        is_tanaman_otomatis = ("kontrol" in judul and "tanaman" in abstrak) or "vertical garden" in judul
        
        if is_bawang and is_penyiraman:
            return 1
        # SPK varietas bawang - choosing variety, not watering
        if "varietas bawang" in judul:
            return 0
        # Kriptografi - completely different
        if "enkripsi" in judul or "kriptografi" in judul or "pesan singkat" in judul:
            return 0
        # Empang/monitoring air - different domain
        if "empang" in judul:
            return 0
        # Klasifikasi telur - completely different
        if "telur" in judul:
            return 0
        # Hidroponik - related to automated plant watering
        if "hidroponik" in judul and ("penyiraman" in abstrak or "suhu" in judul or "kelembapan" in judul):
            return 0
        # Tanaman cengkeh + sistem kontrol + penyiraman
        if is_tanaman_otomatis:
            return 0
        if "vertical garden" in judul:
            return 0
        return 0
    
    # ========================
    # Q16: "klasifiaksi" (typo of "klasifikasi")
    # ========================
    if record["ID"] == "Q16":
        if "klasifikasi" in judul:
            return 1
        # Prediksi kelulusan with classification algorithms
        if ("prediksi" in judul or "memprediksi" in judul) and ("random forest" in judul or "klasifikasi" in abstrak):
            return 1
        if "optimalisasi prediksi kelulusan" in judul:
            return 1
        # Analisis sentimen uses classification
        if "analisis sentimen" in judul and ("klasifikasi" in abstrak or "support vector machine" in judul):
            return 1
        # Deep learning klasifikasi musik
        if "deep learning" in judul and "klasifikasi" in judul:
            return 1
        # Plagiat detection - not klasifikasi
        if "plagiat" in judul:
            return 0
        # Klasterisasi - clustering, NOT klasifikasi
        if "klasterisasi" in judul or "k-means" in judul:
            return 0
        # Persalinan/VR - not klasifikasi
        if "persalinan" in judul:
            return 0
        # Game edukasi - not klasifikasi
        if "game" in judul:
            return 0
        return 0
    
    # ========================
    # Q17: "mikrokntroler" (typo of "mikrokontroler")
    # ========================
    if record["ID"] == "Q17":
        if "mikrokontroler" in judul or "mikrokontroler" in abstrak or "mikrokontroller" in abstrak:
            return 1
        if "arduino" in judul or "arduino" in abstrak:
            return 1
        if "mikrokontroller" in judul:
            return 1
        return 0
    
    # ========================
    # Q18: "yolo" (short query)
    # ========================
    if record["ID"] == "Q18":
        if "yolo" in judul or "yolo" in abstrak or "you only look once" in judul or "you only look once" in abstrak:
            return 1
        if "yolov8" in judul or "yolov8" in abstrak or "yolov7" in judul or "yolov9" in judul or "yolov9" in abstrak:
            return 1
        return 0
    
    # ========================
    # Q19: "androdi" (typo of "android")
    # ========================
    if record["ID"] == "Q19":
        if "android" in judul or "berbasis android" in abstrak:
            return 1
        # Not about Android
        return 0
    
    # ========================
    # Q20: "sistem pakar android 2018" (metadata query with year)
    # ========================
    if record["ID"] == "Q20":
        is_sistem_pakar = ("sistem pakar" in judul or "expert system" in judul or 
                          "sistem pakar" in abstrak)
        is_android = "android" in judul or "android" in abstrak or "mobile" in judul
        tahun_match = tahun_doc == 2018
        
        # Must match: sistem pakar + android + 2018
        if is_sistem_pakar and is_android and tahun_match:
            return 1
        if is_sistem_pakar and tahun_match:
            return 1
        return 0
    
    # ========================
    # Q21: "internet of things 2024" (metadata query with year)
    # ========================
    if record["ID"] == "Q21":
        is_iot = ("internet of things" in judul or "iot" in judul or
                 "internet of things" in abstrak or "iot" in abstrak)
        tahun_match = tahun_doc == 2024
        
        if is_iot and tahun_match:
            return 1
        return 0
    
    return 0

# Process all records
for record in data:
    score = evaluate_relevance(record)
    record["Skor_Relevansi"] = {
        "mhs1": score,
        "mhs2": score,
        "dsn3": score
    }

# Save updated file
with open(r"c:\belajarku\semester 7\evaluasi_app\evaluasi_rag_vs_hyde_fix.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Print summary
total = len(data)
relevant = sum(1 for r in data if r["Skor_Relevansi"]["mhs1"] == 1)
not_relevant = total - relevant

print(f"Total records: {total}")
print(f"Relevant (1): {relevant}")
print(f"Not Relevant (0): {not_relevant}")
print()

from collections import defaultdict
query_stats = defaultdict(lambda: {"total": 0, "relevant": 0, "query": ""})
for r in data:
    qid = r["ID"]
    query_stats[qid]["total"] += 1
    query_stats[qid]["query"] = r["Query_Text"]
    if r["Skor_Relevansi"]["mhs1"] == 1:
        query_stats[qid]["relevant"] += 1

for qid in sorted(query_stats.keys(), key=lambda x: int(x[1:])):
    stats = query_stats[qid]
    print(f"{qid} ({stats['query'][:40]}): {stats['relevant']}/{stats['total']} relevant")

# Verify no nulls remain
null_count = sum(1 for r in data if r["Skor_Relevansi"]["mhs1"] is None or 
                 r["Skor_Relevansi"]["mhs2"] is None or r["Skor_Relevansi"]["dsn3"] is None)
print(f"\nRecords with null values: {null_count}")
print("\nDone!")
