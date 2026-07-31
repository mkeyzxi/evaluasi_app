### Kriteria Relevansi dan Konstruksi *Ground Truth*

Evaluasi terhadap metrik *Precision@k*, *Recall@k*, dan *Mean Reciprocal Rank* (MRR) dalam penelitian ini mengacu pada *ground truth* berbasis relevansi biner, yaitu nilai **1 (Relevan)** dan nilai **0 (Tidak Relevan)**. Mengingat karakteristik *query* yang bersifat pendek (1–5 kata) dan menggunakan bahasa kasual, penentuan nilai relevansi tidak dilakukan secara eliminasi kaku (*strict elimination*), melainkan melalui pendekatan evaluasi holistik dengan mempertimbangkan fleksibilitas semantik serta niat utama (*search intent*) pengguna dalam domain Teknik Informatika dan Sistem Informasi.

Sebuah dokumen skripsi dinilai relevan (1) atau tidak relevan (0) berdasarkan tiga kriteria kelayakan yang ditimbang secara bersamaan:

#### 1. Kesesuaian Fokus Konseptual (*Conceptual Focus Alignment*)

Kriteria ini menilai apakah dokumen berada pada payung topik dan objek penelitian yang sama dengan *query*.

- **Relevan (1):** Jika entitas atau objek utama pada *query* (seperti *kualitas air*, *penyakit tanaman*, atau *penerima bantuan*) bertindak sebagai fokus utama, variabel terikat, atau hasil luaran (*output*) dari penelitian yang dijelaskan dalam judul dan abstrak.
- **Tidak Relevan (0):** Jika entitas pada *query* hanya disebutkan sebagai latar belakang umum, tinjauan pustaka sekilas, studi terdahulu, atau saran untuk pengembangan sistem selanjutnya (*future work*).

#### 2. Kesesuaian Fungsional dan Domain Masalah (*Functional & Domain Alignment*)

Kriteria ini menilai tingkat keselarasan fungsi operasional sistem dengan kebutuhan masalah pada *query*.

- **Relevan (1):** Dokumen memecahkan kategori masalah dalam domain yang sama. Untuk *query* kasual/pendek berbasis otomatisasi atau IoT, dokumen yang menyediakan fungsionalitas pendukung langsung (*monitoring* atau pemantauan) terhadap *query* bertema tindakan (*kontrol* atau pengaturan) dinilai **relevan (1)**, selama beroperasi pada objek dan tujuan masalah yang sama persis (misal: *monitoring* kualitas air untuk *query* pengaturan air kolam).
- **Tidak Relevan (0):** Dokumen gugur jika fungsi operasionalnya berbeda secara fundamental dan berada pada domain aplikasi yang berseberangan, seperti *query* pencarian "media pembelajaran" yang mengembalikan dokumen "sistem administrasi/manajemen".

#### 3. Spesifisitas Leksikal dan Atribut Teknis (*Lexical Specificity & Technical Attribute Alignment*)

Kriteria ini menangani *query* yang menyertakan atribut teknik, nama metode, atau algoritma spesifik.

- **Penggunaan Algoritma Spesifik:** Jika *query* menyebutkan nama algoritma komputasi secara eksplisit (seperti *"Convolutional Neural Network"*, *"AHP"*, atau *"Dijkstra"*), maka dokumen **wajib** mengimplementasikan algoritma tersebut. Ketiadaan algoritma spesifik pada dokumen mengakibatkan dokumen dinilai **0**.
- **Penggunaan Token Umum ("Metode"):** Jika *query* hanya memuat token umum seperti kata *"metode"* tanpa menyebutkan nama spesifik, dokumen dinilai **relevan (1)** apabila mengimplementasikan minimal satu metode komputasi, algoritma kecerdasan buatan, atau algoritma pemrosesan data (seperti algoritma klasifikasi, *forecasting*, atau sistem pakar). Metode pengembangan perangkat lunak umum (seperti *Waterfall* atau *Agile*) serta metode pengumpulan data (seperti wawancara) **tidak dapat** dijadikan dasar tunggal pemenuhan kriteria ini.