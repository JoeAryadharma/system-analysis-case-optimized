# Laporan Analisis Keamanan Aspek Eksternal (External Security Analysis)
**Sistem Pengadaan Barang (SIPB) Lintas Platform**

Laporan ini menyusun arsitektur dan strategi mitigasi ancaman keamanan dari aspek eksternal terhadap Sistem Pengadaan Barang (SIPB) pada platform Web App, Android, dan iOS di bawah pengawasan **Kernel Joe Aryadharma**.

---

## 1. Keamanan Jaringan & Lapisan Transportasi (Network Security)

Ancaman eksternal terbesar pada lalu lintas data adalah penyadapan pihak ketiga (*Eavesdropping*) dan serangan *Man-in-the-Middle (MitM)*.

*   **Penerapan TLS 1.3 / HTTPS**:
    *   Seluruh komunikasi data antara aplikasi (Web, Android, iOS) dengan server API wajib menggunakan HTTPS dengan konfigurasi TLS 1.3 minimum. Algoritma enkripsi lemah (seperti RC4, 3DES) wajib dinonaktifkan di sisi web server/Vercel.
*   **SSL Pinning (Mobile Native)**:
    *   Pada aplikasi Android (Kotlin) dan iOS (Swift), metode *SSL Pinning* harus diterapkan untuk mengunci sertifikat kriptografi server API tujuan secara langsung di dalam kode biner aplikasi. Ini memblokir aplikasi dari mempercayai sertifikat *Self-Signed* palsu yang disisipkan oleh peretas di jaringan publik (misalnya, di Wi-Fi publik).

---

## 2. Perlindungan Terhadap Serangan Web (OWASP Top 10 Mitigation)

Aplikasi web PWA dan server API dilindungi dari serangan eksternal yang mengeksploitasi celah aplikasi:

*   **Cross-Site Scripting (XSS) Mitigation**:
    *   Setiap data teks masukan dari vendor atau peran eksternal disaring ketat melalui metode *Sanitization* sebelum dirender ke DOM HTML. 
    *   Penerapan header **Content Security Policy (CSP)** secara ketat di sisi server untuk melarang eksekusi *inline script* yang tidak sah dan membatasi asal domain pemanggilan library eksternal.
*   **Cross-Origin Resource Sharing (CORS)**:
    *   Kebijakan CORS diatur secara eksplisit untuk hanya mengizinkan permintaan API dari asal domain terdaftar aplikasi web resmi (misalnya, `https://web-app-ashy-nu.vercel.app`) dan memblokir seluruh origin tidak dikenal (*Origin wildcard `*` dilarang keras*).
*   **Perlindungan CSRF (Cross-Site Request Forgery)**:
    *   Setiap request mutasi data (pengajuan, PKS, pencairan) diwajibkan menyertakan *CSRF Token* kriptografis unik di dalam header HTTP request untuk memverifikasi bahwa permintaan tersebut benar-benar berasal dari interaksi pengguna aktif di aplikasi resmi.

---

## 3. Keamanan Platform Mobile Native (Mobile Security)

Aplikasi mobile (Android/iOS) rentan terhadap dekompilasi (*Reverse Engineering*) dan modifikasi runtime:

*   **Obfuskasi Kode (Code Obfuscation)**:
    *   *Android*: Mengaktifkan compiler **R8/ProGuard** untuk mereduksi dan mengacak penamaan kelas, variabel, dan metode menjadi karakter acak sehingga menyulitkan peretas yang mendekompilasi file APK menjadi kode sumber asli.
    *   *iOS*: Menggunakan pengoptimal Swift compiler dan meniadakan simbol debugging pada file *Archive* sebelum dikompilasi menjadi IPA.
*   **Deteksi Perangkat Rooted / Jailbroken**:
    *   Aplikasi mendeteksi keberadaan biner *SuperUser* (Android) atau *Cydia/Sileo* (iOS). Jika perangkat terdeteksi telah dimodifikasi (Root/Jailbreak), aplikasi akan otomatis menutup sesi login demi melindungi data persistensi sensitif dari penyadapan sistem operasi yang tidak aman.
*   **Secure Storage (Enkripsi Data Lokal)**:
    *   Data sesi lokal tidak boleh disimpan dalam bentuk teks biasa. Android menggunakan **EncryptedSharedPreferences** (Android Jetpack Security) dan iOS menggunakan **Apple Keychain Services** berbasis enkripsi tingkat perangkat keras (*Secure Enclave*).

---

## 4. Perlindungan Aset Digital & Serverless Infrastructure

*   **Rate Limiting & DDoS Mitigation**:
    *   Infrastruktur penyebaran di-hosting menggunakan jaringan tepi edge network (Vercel Edge Network / Cloudflare WAF) yang secara otomatis menyaring serangan banjir lalu lintas (DDoS) dan membatasi jumlah request per IP (*Rate Limiting*) menjadi maksimal 100 request/menit untuk mencegah serangan brute force.
*   **Keamanan Storage PO & Invoice**:
    *   Berkas PO/Invoice yang diunggah dilarang diletakkan di folder publik yang dapat diakses langsung via tautan URL tebakan. Seluruh aset diletakkan di Cloud Storage Bucket privat dengan otorisasi berbasis token bertanda tangan dinamis (*Signed URL*) dengan masa kedaluwarsa maksimal 15 menit.

---

## 5. Kesimpulan Audit Keamanan Eksternal
Melalui penerapan **SSL Pinning**, **ProGuard/R8 Obfuscation**, enkripsi data lokal (**Keychain/EncryptedSharedPreferences**), dan kebijakan **CORS/CSP** yang ketat, celah serangan dari aspek eksternal dapat diminimalisir hingga ke tingkat *Low-Risk*. Audit penetrasi eksternal (*External Penetration Testing*) berkala direkomendasikan setiap kali merilis fitur berskala besar.
