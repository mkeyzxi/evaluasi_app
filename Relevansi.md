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

Kriteria ini bersifat kondisional dan dieksekusi **hanya** jika *query* pengguna menyertakan atribut teknis, nama metode, atau algoritma.

- **Penggunaan Algoritma atau Teknologi Spesifik (*Exact Match*):**
Jika *query* menyebutkan nama algoritma, metode, atau *framework* komputasi secara eksplisit dan spesifik (seperti *"Convolutional Neural Network"*, *"AHP"*, *"Dijkstra"*, atau *"Flutter"*), maka dokumen **wajib mutlak** mengimplementasikan teknologi tersebut sebagai instrumen utama atau parameter pengujian penelitian. Ketiadaan atribut spesifik ini pada abstrak dan judul mengakibatkan dokumen otomatis digugurkan dan dinilai **Tidak Relevan (0)**, terlepas dari seberapa identik objek masalahnya dengan *query*.
- **Penggunaan Token Leksikal Umum (*General Intent*):**
Jika *query* hanya memuat token umum tanpa spesifikasi leksikal (seperti murni menggunakan kata *"metode"*, *"algoritma"*, atau *"sistem"*), dokumen dinilai **Relevan (1)** selama mengimplementasikan pendekatan metodologis yang menjadi nilai inti (*core value*) penyelesaian masalah dari penelitian. Ruang lingkup ini sah mencakup algoritma kecerdasan buatan, metode analitik/komputasi, **serta metode rekayasa perangkat lunak dan pengembangan sistem (seperti *Agile*, *Scrum*, *User-Centered Design*, dll.)**. Pengguguran dokumen rekayasa perangkat lunak secara sepihak untuk *query* umum tidak dibenarkan karena akan mendistorsi dan memanipulasi probabilitas tangkapan sistem (*Recall*).