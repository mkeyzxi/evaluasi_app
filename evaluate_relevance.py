import json

with open(r"c:\belajarku\semester 7\evaluasi_app\evaluasi_model.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def evaluate_relevance(record):
    query = record.get("Query_Text", "").lower()
    judul = record.get("Judul_Skripsi", "").lower()
    abstrak = record.get("Abstrak", "").lower()
    tahun_doc = record.get("Tahun", 0)
    
    qid = record.get("ID", "")
    
    def check_keywords(keywords_list, text):
        return any(kw in text for kw in keywords_list)
        
    def match(judul_keywords, abstrak_keywords=[]):
        j_match = all(check_keywords(kws, judul) for kws in judul_keywords) if judul_keywords else True
        a_match = all(check_keywords(kws, abstrak) for kws in abstrak_keywords) if abstrak_keywords else True
        return j_match and a_match

    # Base match logic based on QID
    if qid == "Q01": # sistem pendukung keputusan metode
        if check_keywords(["sistem pendukung keputusan", "spk"], judul) or check_keywords(["sistem pendukung keputusan", "spk"], abstrak): return 1
    elif qid == "Q02": # aplikasi media pembelajaran android
        if check_keywords(["pembelajaran", "edukasi"], judul) and check_keywords(["android", "aplikasi", "mobile"], judul + abstrak): return 1
    elif qid == "Q03": # algoritma convolutional neural network
        if check_keywords(["convolutional neural network", "cnn"], judul + abstrak): return 1
    elif qid == "Q04": # sistem kontrol berbasis iot
        if check_keywords(["iot", "internet of things", "kontrol", "monitoring"], judul + abstrak) and check_keywords(["kontrol", "monitoring"], judul): return 1
    elif qid == "Q05": # sistem pakar diagnosa penyakit
        if check_keywords(["sistem pakar", "expert system"], judul) and check_keywords(["diagnosa", "penyakit"], judul + abstrak): return 1
    elif qid == "Q06": # sistem question answering chatbot
        if check_keywords(["chatbot", "question answering", "tanya jawab"], judul + abstrak): return 1
    elif qid == "Q07": # analisis sentimen word embedding
        if check_keywords(["sentimen"], judul) and check_keywords(["word embedding", "word2vec", "fasttext", "glove"], judul + abstrak): return 1
    elif qid == "Q08": # penerapan progressive web application
        if check_keywords(["progressive web", "pwa"], judul + abstrak): return 1
    elif qid == "Q09": # algoritma k-nearest neighbor
        if check_keywords(["k-nearest", "knn"], judul + abstrak): return 1
    elif qid == "Q10": # metode full-text indexing
        if check_keywords(["full-text", "indexing", "pencarian"], judul + abstrak): return 1
    elif qid == "Q11": # klasifikasi kematangan buah cabai cnn
        if check_keywords(["cabai", "cabe"], judul + abstrak) and check_keywords(["cnn", "convolutional neural network", "klasifikasi", "kematangan"], judul + abstrak): return 1
    elif qid == "Q12": # vehicle routing problem logistik waktu
        if check_keywords(["vehicle routing", "vrp", "rute", "logistik", "waktu"], judul + abstrak) and check_keywords(["vehicle routing", "vrp"], judul + abstrak): return 1
    elif qid == "Q13": # kualitas sarang burung walet vgg16
        if check_keywords(["walet"], judul + abstrak) and check_keywords(["vgg16", "kualitas", "sarang"], judul + abstrak): return 1
    elif qid == "Q14": # pakan lele otomatis iot
        if check_keywords(["lele"], judul + abstrak) and check_keywords(["pakan", "otomatis", "iot", "internet of things"], judul + abstrak): return 1
    elif qid == "Q15": # pengenalan jenis kulit wajah vgg16
        if check_keywords(["kulit wajah", "wajah"], judul + abstrak) and check_keywords(["vgg16", "pengenalan", "jenis"], judul + abstrak): return 1
    elif qid == "Q16": # klasifikasi fertilitas telur ayam yolov8
        if check_keywords(["telur"], judul + abstrak) and check_keywords(["fertilitas", "yolov8", "klasifikasi", "yolo"], judul + abstrak): return 1
    elif qid == "Q17": # water resistant perkebunan karet mikrokontroler
        if check_keywords(["karet"], judul + abstrak) and check_keywords(["water resistant", "mikrokontroler", "arduino"], judul + abstrak): return 1
    elif qid == "Q18": # sentimen ulasan wisata pantai losari lstm
        if check_keywords(["sentimen"], judul + abstrak) and check_keywords(["wisata", "losari", "pantai", "lstm"], judul + abstrak): return 1
    elif qid == "Q19": # animasi struktur bumi augmented reality
        if check_keywords(["animasi", "struktur bumi", "bumi", "geografi"], judul + abstrak) and check_keywords(["augmented reality", "ar", "3d"], judul + abstrak): return 1
    elif qid == "Q20": # deteksi kelelawar mikrokontroler android
        if check_keywords(["kelelawar"], judul + abstrak): return 1
    elif qid == "Q21": # cara otomatis pisahin telur bagus
        if check_keywords(["telur"], judul + abstrak) and check_keywords(["pemilahan", "penyortir", "klasifikasi", "otomatis", "kualitas"], judul + abstrak): return 1
    elif qid == "Q22": # alat biar motor gak gampang dicuri
        if check_keywords(["sepeda motor", "motor", "kendaraan bermotor"], judul) and check_keywords(["keamanan", "pengamanan", "pencurian", "fingerprint", "nfc", "anti maling"], judul + abstrak): return 1
    elif qid == "Q23": # bikin aplikasi donasi untuk pelosok
        if check_keywords(["donasi", "penggalangan dana", "bantuan", "charity"], judul + abstrak): return 1
    elif qid == "Q24": # aplikasi buat hafalan quran santri
        if check_keywords(["quran", "qur'an", "hafalan", "tahfidz", "tajwid"], judul + abstrak): return 1
    elif qid == "Q25": # gimana cara siram bawang otomatis
        if check_keywords(["bawang"], judul + abstrak) and check_keywords(["siram", "penyiraman", "otomatis", "kontrol"], judul + abstrak): return 1
    elif qid == "Q26": # website buat cari info kos
        if check_keywords(["kos", "indekos", "kost"], judul + abstrak) and check_keywords(["website", "web", "sistem informasi", "pencarian", "aplikasi"], judul + abstrak): return 1
    elif qid == "Q27": # alat biar sapi tidak dicuri
        if check_keywords(["sapi", "ternak"], judul + abstrak) and check_keywords(["keamanan", "pencurian", "monitoring", "lokasi", "gps"], judul + abstrak): return 1
    elif qid == "Q28": # bantu tunanetra tahu nominal uang
        if check_keywords(["tunanetra", "buta"], judul + abstrak) and check_keywords(["uang", "nominal", "pengenalan", "deteksi", "mata uang"], judul + abstrak): return 1
    elif qid == "Q29": # aplikasi lapor fasilitas publik rusak
        if check_keywords(["fasilitas publik", "infrastruktur", "pengaduan", "pelaporan", "jalan rusak", "lapor"], judul + abstrak): return 1
    elif qid == "Q30": # cara cek tugas akhir plagiat
        if check_keywords(["plagiat", "plagiarisme", "kemiripan", "tugas akhir", "skripsi", "dokumen"], judul + abstrak) and check_keywords(["plagiat", "kemiripan", "plagiarisme"], judul + abstrak): return 1
    elif qid == "Q31": # klasifiaksi
        if check_keywords(["klasifikasi", "pengelompokan"], judul + abstrak): return 1
    elif qid == "Q32": # mikrokntroler
        if check_keywords(["mikrokontroler", "mikrokontroller", "arduino", "esp", "nodemcu"], judul + abstrak): return 1
    elif qid == "Q33": # yolo
        if check_keywords(["yolo", "you only look once", "yolov"], judul + abstrak): return 1
    elif qid == "Q34": # androdi
        if check_keywords(["android"], judul + abstrak): return 1
    elif qid == "Q35": # algorimta
        if check_keywords(["algoritma", "metode"], judul + abstrak): return 1
    elif qid == "Q36": # k-menas
        if check_keywords(["k-means", "kmeans", "k means"], judul + abstrak): return 1
    elif qid == "Q37": # naiv bayes
        if check_keywords(["naive bayes", "naïve bayes", "naiv bayes"], judul + abstrak): return 1
    elif qid == "Q38": # blokchain
        if check_keywords(["blockchain", "rantai blok"], judul + abstrak): return 1
    elif qid == "Q39": # frameowrk
        if check_keywords(["framework", "kerangka kerja", "laravel", "codeigniter", "flutter", "react"], judul + abstrak): return 1
    elif qid == "Q40": # pwa
        if check_keywords(["pwa", "progressive web app", "progressive web application"], judul + abstrak): return 1
    elif qid == "Q41": # sistem pakar android 2018
        if check_keywords(["sistem pakar", "expert system"], judul + abstrak) and check_keywords(["android", "mobile"], judul + abstrak) and (tahun_doc == 2018 or '2018' in judul + abstrak): return 1
    elif qid == "Q42": # internet of things 2024
        if check_keywords(["iot", "internet of things"], judul + abstrak) and (tahun_doc == 2024 or '2024' in judul + abstrak): return 1
    elif qid == "Q43": # augmented reality 2017
        if check_keywords(["augmented reality", "ar"], judul + abstrak) and (tahun_doc == 2017 or '2017' in judul + abstrak): return 1
    elif qid == "Q44": # sistem pendukung keputusan 2020
        if check_keywords(["sistem pendukung keputusan", "spk"], judul + abstrak) and (tahun_doc == 2020 or '2020' in judul + abstrak): return 1
    elif qid == "Q45": # convolutional neural network 2025
        if check_keywords(["convolutional neural network", "cnn"], judul + abstrak) and (tahun_doc == 2025 or '2025' in judul + abstrak): return 1
    elif qid == "Q46": # aplikasi rumah sakit 2021
        if check_keywords(["rumah sakit", "rsud", "klinik", "puskesmas"], judul + abstrak) and (tahun_doc == 2021 or '2021' in judul + abstrak): return 1
    elif qid == "Q47": # progressive web app 2022
        if check_keywords(["progressive web", "pwa"], judul + abstrak) and (tahun_doc == 2022 or '2022' in judul + abstrak): return 1
    elif qid == "Q48": # algoritma k-means 2024
        if check_keywords(["k-means", "kmeans", "k means"], judul + abstrak) and (tahun_doc == 2024 or '2024' in judul + abstrak): return 1
    elif qid == "Q49": # mikrokontroler arduino 2019
        if check_keywords(["mikrokontroler", "arduino"], judul + abstrak) and (tahun_doc == 2019 or '2019' in judul + abstrak): return 1
    elif qid == "Q50": # sistem pakar web 2017
        if check_keywords(["sistem pakar", "expert system"], judul + abstrak) and check_keywords(["web", "website"], judul + abstrak) and (tahun_doc == 2017 or '2017' in judul + abstrak): return 1

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
with open(r"c:\belajarku\semester 7\evaluasi_app\evaluasi_model.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Print summary
total = len(data)
relevant = sum(1 for r in data if r["Skor_Relevansi"]["mhs1"] == 1)
not_relevant = total - relevant

print(f"Total records: {total}")
print(f"Relevant (1): {relevant}")
print(f"Not Relevant (0): {not_relevant}\n")

from collections import defaultdict
query_stats = defaultdict(lambda: {"total": 0, "relevant": 0, "query": ""})
for r in data:
    qid = r["ID"]
    query_stats[qid]["total"] += 1
    query_stats[qid]["query"] = r.get("Query_Text", "")
    if r["Skor_Relevansi"]["mhs1"] == 1:
        query_stats[qid]["relevant"] += 1

for qid in sorted(query_stats.keys(), key=lambda x: int(x[1:]) if x[1:].isdigit() else 999):
    stats = query_stats[qid]
    print(f"{qid} ({stats['query'][:40]}): {stats['relevant']}/{stats['total']} relevant")

print("\nDone!")
