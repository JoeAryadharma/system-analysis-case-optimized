# Aplikasi SIPB Ter-optimasi & Laporan Analisis Lanjutan (Optimized Version)
**Kandidat: Joe Aryadharma (System Analyst & Developer)**

Selamat datang di direktori utama untuk solusi teknis **Sistem Informasi Pengadaan Barang (SIPB)**. Folder ini berisi kode sumber aplikasi siap rilis untuk platform Web (PWA), Android, dan iOS yang terintegrasi dengan database awan Supabase, serta dokumen analisis taktis tambahan.

---

## 🚀 Uji Coba Cepat Aplikasi (Hanya 3 Langkah!)

Anda dapat menguji kelancaran sistem ini secara instan:

### 1. Buka Aplikasi Web Live
Akses prototipe web resmi melalui tautan berikut:
👉 **[test-case-system-analysis-case.vercel.app](https://test-case-system-analysis-case.vercel.app)**

### 2. Gunakan Fitur Quick Login
Di halaman masuk (*login*), Anda tidak perlu mengetik. Cukup klik salah satu tombol peran di bawah form untuk langsung masuk:
* 👤 **Pemohon** (Pengaju pengadaan)
* 🛠️ **Procurement** (Penyusun kontrak & termin)
* 💰 **Budgeting** (Penyetuju pagu anggaran unit)
* 🏦 **Keuangan** (Pencatat invoice vendor)
* 💵 **Kasir** (Pencair dana & debet kas riil)

*(Gunakan password universal **`admin123`** jika meminta masukan manual).*

### 3. Pasang di Smartphone Android (Instalasi APK)
Unduh dan pasang berkas biner aplikasi Android langsung di ponsel Anda:
📲 **[Unduh sipb-mobile.apk](bin/sipb-mobile.apk)**

---

## 📂 Struktur Berkas Direktori
* 📁 **`/apps/web-app`**: Kode program web PWA (HTML, CSS, JS) dengan Supabase Client SDK.
* 📁 **`/apps/sipb-android`**: Kode program aplikasi Android native (Jetpack Compose).
* 📁 **`/apps/sipb-ios`**: Aset antarmuka iOS native.
* 📁 **`/laporan`**: Berkas dokumen PDF laporan Tugas 1-5 versi ter-optimasi (bebas ISO, dilengkapi RACI, Story Points, operational risk register, audit keamanan eksternal, dan Laporan Penyerahan Resmi).
* 📁 **`/database`**: Berkas skema SQL DDL Supabase (`supabase_schema.sql`).
* 📁 **`/bin`**: Berkas biner instalasi Android (`sipb-mobile.apk`).

---

## 🔗 Tautan Cepat
* 🌐 **Aplikasi Web Live (Optimized)**: [Buka Aplikasi](https://test-case-system-analysis-case.vercel.app)
* ⚙️ **Skema SQL Supabase**: [Lihat database/supabase_schema.sql](database/supabase_schema.sql)
