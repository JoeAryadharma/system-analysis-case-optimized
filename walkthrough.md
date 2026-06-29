# Walkthrough: Rilis Sistem Pengadaan Barang (SIPB) Terintegrasi Login, RBAC, & Supabase
**Kernel Joe Aryadharma Operational Report**

Pembangunan ulang aplikasi Web, Android Native APK, dan iOS Native dari awal telah selesai dirancang, diintegrasikan, dan di-deploy secara online dengan dukungan autentikasi Login, Role-Based Access Control (RBAC), serta integrasi **Supabase Cloud Database**.

---

## 1. Tautan Aplikasi Live Daring (PWA)

Kami menyediakan dua versi aplikasi web yang terpisah di Vercel untuk mempermudah perbandingan:

*   🚀 **[Web App Versi Optimized (Dengan Optimasi & Supabase)](https://test-case-system-analysis-case.vercel.app)**  
    *Tautan Alternatif: [https://web-app-ashy-nu.vercel.app](https://web-app-ashy-nu.vercel.app)*
*   ⚖️ **[Web App Versi Default (Tanpa Optimasi)](https://test-case-system-analysis-case-default.vercel.app)**  
    *Tautan Alternatif: [https://prototype-henna-xi.vercel.app](https://prototype-henna-xi.vercel.app)*

---

## 2. Fitur Baru: Hybrid Database Connection (Supabase Cloud)

Aplikasi kini mendukung **Hybrid Database Mode** untuk mempermudah transisi demonstrasi:
*   **Local Storage Mode (Default)**: Menjalankan demo offline secara instan menggunakan dataset dummy v5 yang melimpah.
*   **Supabase Cloud Mode**: Menghubungkan aplikasi secara langsung ke instance Supabase Cloud Anda secara real-time.
    *   *Penyetelan Koneksi*: Klik tombol **"Database Connection Settings"** di bagian bawah halaman login untuk beralih mode dan memasukkan *Project URL* dan *Anon Key* Supabase Anda.
    *   *Penanda Status Database*: Pojok atas antarmuka (top navbar & sidebar) akan menampilkan indikator badge **`CLOUD`** (warna hijau) saat terhubung ke basis data awan, atau **`LOCAL`** (warna abu-abu) saat offline.

---

## 3. Berkas Deliverables Lokal (Folder Unduhan)

Seluruh deliverables tersimpan secara terstruktur di folder unduhan utama Anda:

📂 **`/Users/user/Downloads/System_Analysis_Case__Joe_Aryadharma/`**

### Berkas Skema SQL Supabase:
*   📄 **[supabase_schema.sql](file:///Users/user/Downloads/System_Analysis_Case__Joe_Aryadharma/supabase_schema.sql)**: Salin seluruh kode DDL di dalam berkas ini ke SQL Editor di dashboard Supabase Anda untuk menginisiasi tabel relasional secara otomatis.

### Pembagian Folder Laporan:

#### A. Folder Laporan Default (Sesuai Tes Awal)
Laporan teoritis awal (Tugas 1-5 PDF & Diagram) yang mencantumkan referensi standar ISO secara eksplisit dan belum dioptimasi dengan tabel-tabel analisis taktis tambahan:
*   📁 **[Default_Test_Report](file:///Users/user/Downloads/System_Analysis_Case__Joe_Aryadharma/Default_Test_Report/)**

#### B. Folder Laporan Ter-optimasi (Optimized Report)
Laporan PDF Tugas 1-5 ter-optimasi (bebas label ISO, dilengkapi matriks RBAC, Story Points, RACI, Skills Mapping, Jalur Kritis, Risk Register) serta dokumen audit tambahan:
*   📁 **[Optimized_Report](file:///Users/user/Downloads/System_Analysis_Case__Joe_Aryadharma/Optimized_Report/)**
    *   📄 *operational_risk_analysis.md* (Laporan Analisis Risiko Operasional)
    *   📄 *external_security_analysis.md* (Laporan Analisis Keamanan Aspek Eksternal)
    *   📄 *supabase_schema.sql* (Salinan Skema SQL Database)

---

## 4. Kredensial Pengujian (Password Universal: `admin123`)

Gunakan panel **Quick Login** (tombol nama peran di form login) untuk simulasi peran secara instan:
*   👤 **Unit Pemohon**: Username `pemohon` (Unit: IT & Infrastructure)
*   🛠️ **Petugas Procurement**: Username `procurement` (Unit: Procurement Division)
*   💰 **Petugas Budgeting**: Username `budgeting` (Unit: Budgeting & Pagu Division)
*   🏦 **Petugas Keuangan**: Username `keuangan` (Unit: Finance Division)
*   💵 **Kasir**: Username `kasir` (Unit: Cashier Division)

---

## 5. Alur Skenario Pengujian End-to-End yang Direkomendasikan

Untuk menguji kelancaran sistem pengadaan barang secara utuh (baik di mode Local maupun Cloud):

1.  **Langkah 1 (Pengajuan)**: Login sebagai **Pemohon**. Klik **"+ Tambah Item"** untuk menginput multi-item barang. Tekan **Kirim**.
2.  **Langkah 2 (Validasi Procurement)**: Logout $\rightarrow$ Login sebagai **Procurement**. Pada menu "Validasi Masuk", klik **Teruskan** untuk menyetujui permintaan Pemohon.
3.  **Langkah 3 (Verifikasi Budgeting)**: Logout $\rightarrow$ Login sebagai **Budgeting**. Di tabel "Verifikasi Anggaran", input nilai estimasi harga pengadaan (misal: `50000000`) dan klik **Setujui** jika sisa pagu unit mencukupi.
4.  **Langkah 4 (Termin PKS)**: Logout $\rightarrow$ Login sebagai **Procurement**. Di menu "Penyusunan Kontrak PKS", klik **Buat Kontrak PKS**. Masukkan nomor kontrak, PO, upload draf PO, tambahkan baris termin bayar (misal: *Termin 1 = 50%, Termin 2 = 50%*). Pastikan akumulasi termin tepat 100% dan klik **Simpan**.
5.  **Langkah 5 (Pencatatan Tagihan)**: Logout $\rightarrow$ Login sebagai **Keuangan**. Pilih nomor Kontrak PKS aktif di dropdown, masukkan nomor invoice vendor, upload berkas invoice vendor, dan klik **Kirim**.
6.  **Langkah 6 (Pencairan Kasir)**: Logout $\rightarrow$ Login sebagai **Kasir**. Pada antrean pencairan dana, masukkan potongan/denda (jika ada), lalu klik **Cairkan**. Sisa pagu anggaran Unit Pemohon akan didebet secara otomatis dan tercatat di **Buku Kas**.
7.  **Langkah 7 (Analitik)**: Masuk ke tab **Analitik** di peran mana saja untuk memantau pembaruan grafik konsumsi anggaran unit aktual secara real-time.
