# Laporan Analisis Risiko Operasional (Operational Risk Analysis)
**Sistem Pengadaan Barang (SIPB) Lintas Platform**

Dokumen ini menyajikan analisis risiko operasional terhadap operasional Sistem Pengadaan Barang (SIPB) pada platform Web App PWA, Android, dan iOS dengan pembatasan akses berbasis peran (RBAC) di bawah pengawasan **Kernel Joe Aryadharma**.

---

## 1. Metodologi Penilaian Risiko
Penilaian risiko dilakukan menggunakan skala kualitatif 5x5 untuk mengukur tingkat kemungkinan terjadinya risiko (*Likelihood*) dan dampak yang ditimbulkan terhadap jalannya operasional bisnis (*Impact*).

$$\text{Skor Risiko} = \text{Likelihood} \times \text{Impact}$$

### Kategori Tingkat Risiko:
*   🟢 **1 - 5 (Low Risk)**: Risiko dapat diterima tanpa tindakan mitigasi khusus, cukup dipantau berkala.
*   🟡 **6 - 12 (Medium Risk)**: Risiko memerlukan tindakan pencegahan terencana dan prosedur standar (SOP).
*   🔴 **15 - 25 (High Risk)**: Risiko kritis yang membutuhkan penanganan segera dan arsitektur pengamanan berlapis.

---

## 2. Matriks Analisis Risiko Operasional

| Kode | Deskripsi Risiko | Dampak Bisnis | Likelihood (1-5) | Impact (1-5) | Skor | Tingkat | Strategi Mitigasi Operasional | PIC Peran |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **R-OPS-01** | Kebocoran data transaksi & draf Kontrak PKS sensitif ke pihak eksternal. | Kehilangan keunggulan kompetitif, pelanggaran kerahasiaan vendor. | 2 | 4 | **8** | 🟡 Medium | Penerapan RBAC ketat, enkripsi file unggahan PO/Invoice di sisi server, enkripsi token sesi. | Procurement / Keuangan |
| **R-OPS-02** | *Session Hijacking* (pembajakan login) atau brute force akun pengujian. | Akses ilegal ke antrean pencairan dana kasir dan persetujuan budgeting. | 3 | 4 | **12** | 🟡 Medium | Pembatasan umur token sesi, penguncian akun otomatis setelah 5 kali salah password, monitoring log IP. | Sistem Admin / IT |
| **R-OPS-03** | Inkonsistensi data anggaran (Sisa pagu tidak terdebet saat Kasir mencairkan dana). | Kebocoran anggaran unit (over-budget), dispute laporan audit Buku Kas. | 1 | 5 | **5** | 🟢 Low | Mekanisme transaksi database atomik (ACID) di local storage, validasi balance sebelum pencairan. | Kasir / Budgeting |
| **R-OPS-04** | Pengajuan ganda (*Double Submission*) pada formulir multi-item Unit Pemohon. | Duplikasi transaksi pengadaan barang, pemborosan sisa pagu unit. | 3 | 3 | **9** | 🟡 Medium | Penonaktifan tombol submit setelah diklik (*Disable Submit Button*), pembuatan hash unik per transaksi. | Unit Pemohon |
| **R-OPS-05** | Kesalahan input termin bayar Kontrak PKS (Persentase termin tidak tepat 100%). | Kesalahan pembayaran vendor, keterlambatan pelunasan, dispute keuangan. | 2 | 4 | **8** | 🟡 Medium | Validasi otomatis di sisi klien (JS validator) yang memblokir tombol simpan jika akumulasi persen $\neq 100\%$. | Procurement |
| **R-OPS-06** | File Invoice yang diunggah Keuangan rusak (*corrupted*) atau palsu. | Hambatan verifikasi pembayaran di Kasir, penundaan pencairan riil. | 3 | 3 | **9** | 🟡 Medium | Validasi tipe file ketat (hanya PDF/PNG), batas maksimal ukuran file 2MB, audit verifikasi visual invoice. | Keuangan / Kasir |
| **R-OPS-07** | Kegagalan server hosting Vercel atau kehilangan koneksi internet lokal (Off-grid). | Operasional pengadaan terhenti, petugas tidak dapat mengakses data antrean. | 2 | 4 | **8** | 🟡 Medium | Implementasi Service Worker PWA untuk caching data luring, sinkronisasi otomatis saat koneksi kembali online. | Developer / DevOps |

---

## 3. Rencana Mitigasi Teknis Detail (SOP Operasional)

### A. Pengamanan Sesi & Otorisasi RBAC (R-OPS-01 & R-OPS-02)
*   **Enkripsi Sesi**: Token sesi yang disimpan di `localStorage` atau `sessionStorage` tidak boleh berupa teks biasa (*plaintext*). Gunakan JWT (JSON Web Token) dengan algoritma enkripsi minimum HS256.
*   **Pembersihan Sesi**: Sesi otomatis dihapus saat browser ditutup atau setelah 30 menit tidak ada aktivitas pengguna (*idle timeout*).

### B. Validasi Konsistensi Anggaran Unit (R-OPS-03 & R-OPS-05)
*   Setiap kali Kasir mengeklik tombol **Cairkan**, sistem wajib melakukan pengecekan ulang:
    $$\text{Sisa Pagu} \ge \text{Nominal Pencairan} - \text{Denda}$$
*   Jika sisa pagu tidak mencukupi, sistem secara otomatis menolak pencairan dan memicu notifikasi peringatan kepada Keuangan dan Budgeting.

### C. Protokol Offline PWA & Auto-Sync (R-OPS-07)
*   Aplikasi web SIPB harus menyematkan berkas `sw.js` (Service Worker) yang mengimplementasikan strategi caching *Stale-While-Revalidate* untuk aset statis dan API offline fallback.
*   Data pengajuan offline disimpan sementara di IndexedDB lokal dan disinkronkan ke server pusat secara otonom saat koneksi internet terdeteksi pulih (`navigator.onLine`).

---

## 4. Kesimpulan & Rekomendasi Audit
Berdasarkan hasil analisis, risiko operasional tertinggi terletak pada **R-OPS-02 (Session Hijacking)** dan **R-OPS-03 (Inkonsistensi Anggaran)**. Implementasi sistem otentikasi dua faktor (2FA) untuk Kasir dan validasi saldo otomatis (debet riil) sangat disarankan untuk mengurangi dampak operasional hingga ke tingkat terendah. Audit log transaksi Buku Kas harus dijalankan minimal setiap akhir kuartal (3 bulanan) secara independen.
