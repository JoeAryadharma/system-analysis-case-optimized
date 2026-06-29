import os
import sys
from fpdf import FPDF

COMPILATION_MODE = 'optimized' # default
if len(sys.argv) > 1 and sys.argv[1] in ['default', 'optimized']:
    COMPILATION_MODE = sys.argv[1]

# Custom FPDF class to implement clean, modern luxury styling (Helvetica & Times)
class SystemAnalysisPDF(FPDF):
    def __init__(self, document_title, doc_code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document_title = document_title
        self.doc_code = doc_code
        self.set_margins(20, 20, 20)
        self.set_auto_page_break(auto=True, margin=20)
        
    def header(self):
        self.set_text_color(31, 41, 55) # Near Black
        
        # Header Top: Document Code / Ref
        self.set_font("Helvetica", "B", 7)
        self.cell(0, 4, f"DOKUMEN SPESIFIKASI  |  KODE REF: {self.doc_code}", ln=True, align="R")
        
        # Title of Project
        self.set_font("Times", "I", 8)
        self.cell(0, 4, "KERNEL JOE ARYADHARMA - SISTEM INFORMASI PENGADAAN BARANG (SIPB)", ln=True, align="L")
        
        # Divider Gold Line
        self.set_draw_color(201, 151, 67) # Gold line
        self.set_line_width(0.5)
        self.line(20, self.get_y() + 2, 190, self.get_y() + 2)
        self.ln(6)

    def footer(self):
        self.set_y(-18)
        self.set_draw_color(229, 231, 235) # Light gray divider
        self.set_line_width(0.3)
        self.line(20, self.get_y(), 190, self.get_y())
        
        self.set_text_color(107, 114, 128) # Gray text
        self.set_font("Helvetica", "I", 7.5)
        
        # Left side: Date/Confidentiality
        self.cell(90, 10, "SIPB SYSTEM REPORT - PROYEK INTERNAL CONFIDENTIAL", align="L")
        # Right side: Page number
        self.cell(80, 10, f"Halaman {self.page_no()}", align="R")

    # Helper for styled Title
    def document_header(self, subtitle=""):
        self.set_text_color(31, 41, 55)
        self.set_font("Times", "B", 18)
        self.multi_cell(0, 8, self.document_title, align="L")
        
        if subtitle:
            self.ln(2)
            self.set_text_color(201, 151, 67) # Gold
            self.set_font("Helvetica", "B", 11)
            self.cell(0, 5, subtitle.upper(), ln=True, align="L")
            
        self.ln(6)
        
    def section_heading(self, text):
        self.set_text_color(31, 41, 55)
        self.set_font("Times", "B", 12)
        self.cell(0, 8, text, ln=True, align="L")
        # Underline accent (Gold)
        self.set_draw_color(201, 151, 67)
        self.set_line_width(0.5)
        self.line(20, self.get_y(), 60, self.get_y())
        self.ln(3)
        
    def paragraph(self, text, style=""):
        self.set_text_color(55, 65, 81) # Dark gray body text
        if style == "bold":
            self.set_font("Helvetica", "B", 9.5)
        elif style == "italic":
            self.set_font("Helvetica", "I", 9.5)
        else:
            self.set_font("Helvetica", "", 9.5)
        self.multi_cell(0, 5, text, align="J")
        self.ln(3.5)
 
    def draw_bullet(self, text, bold_prefix=""):
        self.set_text_color(55, 65, 81)
        self.set_font("Helvetica", "", 9.5)
        self.cell(5, 5, chr(149), align="L") # bullet character
        
        if bold_prefix:
            self.set_font("Helvetica", "B", 9.5)
            self.write(5, bold_prefix + " ")
            self.set_font("Helvetica", "", 9.5)
            
        self.write(5, text)
        self.ln(5)
        
    def add_diagram(self, img_path, w=150, h=0):
        if os.path.exists(img_path):
            self.ln(2)
            x_pos = (210 - w) / 2
            self.image(img_path, x=x_pos, w=w, h=h)
            self.ln(4)
        else:
            self.paragraph(f"[DIAGRAM ERROR: Berkas {img_path} tidak ditemukan]", "italic")

# ================= TUGAS 1: ANALISIS KEBUTUHAN SISTEM =================
def build_pdf_tugas1():
    pdf = SystemAnalysisPDF(
        document_title="Analisis Kebutuhan Sistem & Spesifikasi Antarmuka Pengadaan Barang",
        doc_code="SIPB-T1-SRS"
    )
    pdf.add_page()
    pdf.document_header(subtitle="Tugas 1: Analisis Kebutuhan Awal, RBAC, & Pemodelan Data")
    
    pdf.section_heading("1. Deskripsi Ruang Lingkup Sistem")
    scope_desc = (
        "Sistem Informasi Pengadaan Barang (SIPB) dirancang untuk mengatur, mencatat, dan mengotomatiskan "
        "seluruh alur kerja pengadaan barang di dalam organisasi secara terstruktur dan aman. Sistem ini mencakup "
        "modul autentikasi terisolasi dengan akses kontrol ketat untuk menjamin integritas data dari tahap awal pengajuan "
        "hingga pencairan kasir. Integrasi antarmuka dirancang seragam di semua platform (Web, Android, iOS) "
        "dengan mengedepankan kemudahan pemahaman navigasi bagi pengguna."
    )
    if COMPILATION_MODE == 'default':
        scope_desc += (
            " Perancangan sistem dan arsitektur data antarmuka SIPB ini juga diselaraskan dengan standar kualitas "
            "perangkat lunak ISO/IEC 25010 untuk menjamin kualitas fungsionalitas, kegunaan, keandalan, dan keamanannya."
        )
    pdf.paragraph(scope_desc)
    
    pdf.section_heading("2. Sistem Autentikasi & Hak Akses Berbasis Peran (RBAC)")
    pdf.paragraph(
        "Sistem menerapkan kontrol akses berbasis peran (Role-Based Access Control). Setiap pengguna terdaftar memiliki "
        "satu peran unik dengan hak akses menu yang terisolasi sepenuhnya. Hal ini mencegah tumpang tindih otorisasi dan "
        "melindungi data anggaran organisasi:"
    )
    pdf.draw_bullet("Akses terbatas pada pengajuan permintaan barang multi-item dan monitoring riwayat status.", "1. Peran Unit Pemohon:")
    pdf.draw_bullet("Akses penuh pada validasi permintaan, pembuatan kontrak PKS, input skema termin, dan unggah bukti PO.", "2. Peran Petugas Procurement:")
    pdf.draw_bullet("Akses terbatas pada verifikasi pagu anggaran unit, penyetujuan/penolakan draf, dan riwayat sisa pagu.", "3. Peran Petugas Budgeting:")
    pdf.draw_bullet("Akses terbatas pada pencatatan tagihan masuk, verifikasi rincian barang, dan pengunggahan berkas invoice vendor.", "4. Peran Petugas Keuangan:")
    pdf.draw_bullet("Akses terbatas pada proses pencairan dana final, penginputan denda/potongan kas, dan pencatatan buku kas.", "5. Peran Kasir:")
    pdf.ln(3)

    pdf.paragraph("Tabel Matriks Hak Akses Halaman/Fitur (RBAC Matrix):", "bold")
    
    # RBAC Table
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(243, 244, 246)
    pdf.cell(45, 6, "Halaman / Fitur", border=1, fill=True)
    pdf.cell(21, 6, "Pemohon", border=1, fill=True, align="C")
    pdf.cell(21, 6, "Procurement", border=1, fill=True, align="C")
    pdf.cell(21, 6, "Budgeting", border=1, fill=True, align="C")
    pdf.cell(21, 6, "Keuangan", border=1, fill=True, align="C")
    pdf.cell(21, 6, "Kasir", border=1, fill=True, align="C")
    pdf.ln()
    
    pdf.set_font("Helvetica", "", 7)
    rbac_rows = [
        ("Login & Manajemen Sesi", "YA", "YA", "YA", "YA", "YA"),
        ("Form Permintaan (Multi-item)", "YA (Input)", "TIDAK", "TIDAK", "TIDAK", "TIDAK"),
        ("Validasi & Alasan Tolak", "TIDAK", "YA (Input)", "TIDAK", "TIDAK", "TIDAK"),
        ("Verifikasi Pagu Anggaran", "TIDAK", "TIDAK", "YA (Input)", "TIDAK", "TIDAK"),
        ("Input PKS & Upload PO", "TIDAK", "YA (Input)", "TIDAK", "TIDAK", "TIDAK"),
        ("Catat Tagihan & Upload Invoice", "TIDAK", "TIDAK", "TIDAK", "YA (Input)", "TIDAK"),
        ("Pencairan Kasir & Potongan", "TIDAK", "TIDAK", "TIDAK", "TIDAK", "YA (Input)"),
        ("Laporan Grafik Analitik", "YA (Read)", "YA (Read)", "YA (Read)", "YA (Read)", "YA (Read)")
    ]
    for row in rbac_rows:
        pdf.cell(45, 5.5, row[0], border=1)
        for i in range(1, 6):
            val = row[i]
            if val.startswith("YA"):
                pdf.set_text_color(22, 101, 52) # Dark green
                pdf.set_font("Helvetica", "B", 7)
            else:
                pdf.set_text_color(185, 28, 28) # Red
                pdf.set_font("Helvetica", "", 7)
            pdf.cell(21, 5.5, val, border=1, align="C")
        pdf.ln()
        pdf.set_text_color(55, 65, 81) # reset color
    
    pdf.ln(4)
    pdf.paragraph("Spesifikasi Struktur Data Payload Token Sesi (JSON Payload):", "bold")
    pdf.paragraph(
        "Untuk pertukaran informasi sesi secara aman di seluruh platform web, Android, dan iOS, "
        "digunakan format data payload standard ter-enkripsi di sisi klien sebagai berikut:", "italic"
    )
    
    # JSON Payload Box
    json_text = (
        "{\n"
        "  \"user_id\": \"USR-1092\",\n"
        "  \"username\": \"joe_aryadharma\",\n"
        "  \"role\": \"PROCUREMENT\",\n"
        "  \"authorized_menus\": [\"/dashboard\", \"/validasi\", \"/pks\", \"/laporan\"],\n"
        "  \"exp\": 1782715200\n"
        "}"
    )
    pdf.set_font("Courier", "", 8.5)
    pdf.set_fill_color(249, 250, 251)
    pdf.set_draw_color(229, 231, 235)
    pdf.multi_cell(0, 4.5, json_text, border=1, fill=True)
    pdf.set_draw_color(201, 151, 67) # reset border color
    
    pdf.ln(4)
    pdf.section_heading("3. Diagram Use Case")
    pdf.add_diagram("usecase.png", w=135)
    pdf.paragraph(
        "Diagram Use Case di atas menggambarkan pintu gerbang autentikasi Login (UC0) yang wajib "
        "dilalui oleh kelima aktor untuk mendapatkan otorisasi akses ke menu fungsional masing-masing."
    )
    
    pdf.add_page()
    pdf.section_heading("4. Spesifikasi Kebutuhan Fungsional")
    pdf.paragraph("Kebutuhan fungsional dikelompokkan secara terstruktur berdasarkan peran:")
    pdf.draw_bullet("Sistem harus memvalidasi kredensial pengguna (Username & Password) saat proses login.", "F-001 (Autentikasi):")
    pdf.draw_bullet("Sistem harus membatasi tampilan menu navigasi sesuai peran pengguna yang aktif (RBAC).", "F-002 (Otorisasi):")
    pdf.draw_bullet("Sistem harus menerima pengajuan barang multi-item dari Pemohon (Tanggal, Nama, Jumlah, Satuan).", "F-003 (Permintaan):")
    pdf.draw_bullet("Sistem harus memfasilitasi Procurement melakukan validasi persetujuan atau penolakan bermotif alasan.", "F-004 (Validasi):")
    pdf.draw_bullet("Sistem harus mengirim notifikasi status penolakan langsung ke dashboard Pemohon terkait.", "F-005 (Notifikasi):")
    pdf.draw_bullet("Sistem harus memfasilitasi Budgeting memeriksa status pagu anggaran unit pengaju secara riil.", "F-006 (Verifikasi):")
    pdf.draw_bullet("Sistem harus menyediakan form input detail kontrak PKS (Nomor Kontrak, PO Supplier, Termin Pembayaran).", "F-007 (Kontrak):")
    pdf.draw_bullet("Sistem harus mendukung unggah berkas fisik (PO Supplier dan Invoice Vendor) dengan validasi tipe file.", "F-008 (Berkas):")
    pdf.draw_bullet("Sistem harus memfasilitasi Keuangan mencatat detail tagihan masuk berdasarkan nomor PO.", "F-009 (Tagihan):")
    pdf.draw_bullet("Sistem harus memfasilitasi Kasir mencatat pencairan kasir final beserta potongan/denda.", "F-010 (Pencairan):")
    pdf.draw_bullet("Sistem harus memotong sisa anggaran unit terkait secara otomatis setelah pencairan dana disetujui.", "F-011 (Buku Kas):")
    pdf.draw_bullet("Sistem harus menyajikan grafik analitik konsumsi anggaran unit dan logistik status pengadaan.", "F-012 (Laporan):")
    
    pdf.ln(4)
    pdf.section_heading("5. Alur Transisi Status Transaksi (State Transition Matrix)")
    pdf.paragraph(
        "Untuk memastikan pengembang memahami business logic sistem secara persis, berikut adalah tabel transisi "
        "status dokumen transaksi pengadaan barang dari tahap draf awal hingga lunas:"
    )
    
    # State Transition Table
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(243, 244, 246)
    pdf.cell(32, 6, "Status Asal", border=1, fill=True)
    pdf.cell(48, 6, "Aksi / Pemicu Transisi", border=1, fill=True)
    pdf.cell(32, 6, "Aktor Penanggung Jawab", border=1, fill=True)
    pdf.cell(38, 6, "Status Tujuan", border=1, fill=True)
    pdf.ln()
    
    pdf.set_font("Helvetica", "", 7)
    state_rows = [
        ("N/A", "Mengajukan Permintaan baru", "Unit Pemohon", "PENDING_PROCUREMENT"),
        ("PENDING_PROCUREMENT", "Menolak pengajuan (alasan input)", "Petugas Procurement", "REJECTED_PROCUREMENT"),
        ("PENDING_PROCUREMENT", "Menerima dan meneruskan", "Petugas Procurement", "PENDING_BUDGETING"),
        ("PENDING_BUDGETING", "Menolak pengajuan (anggaran/alasan)", "Petugas Budgeting", "REJECTED_BUDGETING"),
        ("PENDING_BUDGETING", "Menyetujui pagu anggaran", "Petugas Budgeting", "BUDGET_APPROVED"),
        ("BUDGET_APPROVED", "Input kontrak PKS & Upload PO", "Petugas Procurement", "PKS_CONTRACT_CREATED"),
        ("PKS_CONTRACT_CREATED", "Mencatat Invoice Vendor", "Petugas Keuangan", "INVOICE_RECORDED"),
        ("INVOICE_RECORDED", "Mencairkan dana & nominal final", "Kasir", "PAID_COMPLETED")
    ]
    for row in state_rows:
        pdf.cell(32, 5.5, row[0], border=1)
        pdf.cell(48, 5.5, row[1], border=1)
        pdf.cell(32, 5.5, row[2], border=1)
        pdf.cell(38, 5.5, row[3], border=1)
        pdf.ln()
        
    pdf.add_page()
    pdf.section_heading("6. Flowchart Alur Kerja & Navigasi Peran")
    pdf.add_diagram("flowchart.png", w=110)
    pdf.paragraph(
        "Alur kerja di atas menunjukkan aliran proses login autentikasi pengguna di awal, diikuti dengan pengalihan "
        "navigasi antarmuka yang terisolasi untuk memproses alur kerja transaksi pengadaan."
    )
    
    pdf.ln(4)
    pdf.section_heading("7. Entity Relation Diagram (ERD)")
    pdf.add_diagram("erd.png", w=145)
    pdf.paragraph(
        "Untuk memfasilitasi keamanan data dan pengaturan peran, skema database dinormalisasi dengan menambahkan "
        "tabel ROLE dan USER. Kunci relasi (Foreign Key) menghubungkan tabel USER dengan transaksi pengajuan (PERMINTAAN) "
        "sebagai pemohon transaksi secara eksplisit dan ter-audit."
    )
    
    pdf.add_page()
    pdf.section_heading("8. UML Sequence Diagram")
    pdf.add_diagram("sequence.png", w=145)
    pdf.paragraph(
        "Sequence diagram ini menggambarkan interaksi pertukaran pesan autentikasi kredensial antara "
        "Aktor, Antarmuka UI, Controller Sistem, dan database USER untuk membuat token sesi otorisasi."
    )
    
    pdf.section_heading("9. Desain Antarmuka (Mockup Concept)")
    pdf.paragraph(
        "Antarmuka SIPB dirancang modern, sederhana, dan bersih (clean minimalist) dengan sudut tumpul halus "
        "(soft rounded corners) berukuran 6px. Penggunaan font Inter memastikan keterbacaan data yang optimal. "
        "Antarmuka Login dan Dashboard terisolasi per peran disiapkan untuk Web App dan mobile native (Android & iOS). "
        "Prototipe antarmuka terintegrasi ini dapat dibuka langsung pada berkas:"
    )
    pdf.paragraph("web-app/index.html (Buka langsung pada browser komputer atau perangkat mobile)", "bold")
    
    pdf.output("Tugas_1_Analisis_Kebutuhan_Sistem.pdf")
    print("Tugas_1_Analisis_Kebutuhan_Sistem.pdf generated.")

# ================= TUGAS 2: MODEL SDLC =================
def build_pdf_tugas2():
    pdf = SystemAnalysisPDF(
        document_title="Justifikasi Metodologi Siklus Hidup Perangkat Lunak (SDLC)",
        doc_code="SIPB-T2-SDLC"
    )
    pdf.add_page()
    pdf.document_header(subtitle="Tugas 2: Model Proses Pengembangan Sistem (Agile Scrum)")
    
    pdf.section_heading("1. Model Pengembangan Agile Scrum")
    sdlc_desc = (
        "Untuk mengimplementasikan Sistem Informasi Pengadaan Barang (SIPB) pada 3 platform berbeda (Web, Android, iOS) "
        "dalam tenggat waktu yang sangat ketat yaitu 3 bulan (12 minggu), dipilih metodologi Agile Scrum. Pendekatan "
        "iteratif ini sangat efektif untuk membagi pengerjaan menjadi sprint berdurasi 2 minggu, sehingga "
        "penyesuaian kebutuhan fungsional dan pengujian keamanan dapat dilakukan secara terus-menerus."
    )
    if COMPILATION_MODE == 'default':
        sdlc_desc += (
            " Pemilihan model proses pengembangan ini diselaraskan dengan kaidah siklus hidup pengembangan "
            "perangkat lunak standar ISO/IEC 12207 guna menjamin keandalan kontrol kualitas tahapan pengujian."
        )
    pdf.paragraph(sdlc_desc)
    
    pdf.section_heading("2. Justifikasi Pemilihan Metode")
    pdf.paragraph(
        "Penggunaan Agile Scrum memberikan jaminan kecepatan dan fleksibilitas selama siklus hidup proyek:"
    )
    pdf.draw_bullet(
        "Dalam batasan 3 bulan, sangat berisiko menggunakan Waterfall karena kegagalan integrasi baru diketahui di akhir. "
        "Dengan membagi waktu menjadi 6 Sprint, fungsionalitas utama (Minimum Viable Product - MVP) dapat diselesaikan "
        "dan diverifikasi mutunya secara bertahap.",
        "Batasan Waktu Ketat (12 Minggu):"
    )
    pdf.draw_bullet(
        "Sistem ini melibatkan 5 aktor pengguna yang terisolasi dengan RBAC. Pertemuan Sprint Review di akhir setiap "
        "sprint memfasilitasi demo antarmuka langsung kepada masing-masing perwakilan pengguna untuk mendapatkan feedback instan.",
        "Kolaborasi dan Otorisasi Multi-Peran:"
    )
    pdf.draw_bullet(
        "Alur pengadaan melibatkan integrasi unggah berkas PO fisik dan Invoice Vendor. Fleksibilitas backlog pada "
        "Scrum memungkinkan pengembang melakukan penyesuaian prioritas pengerjaan di Sprint berikutnya jika ditemukan kendala "
        "teknis pemrosesan format dokumen.",
        "Adaptabilitas terhadap Berkas Eksternal:"
    )
    pdf.draw_bullet(
        "Fitur login autentikasi dan otorisasi menu (RBAC) diposisikan sebagai prioritas utama (Sprint 1), "
        "sehingga jaminan keamanan data transaksi dan pagu anggaran telah teruji sejak awal sebelum fitur transaksi lainnya didevelop.",
        "Pendekatan Security-First:"
    )
    
    pdf.ln(4)
    pdf.section_heading("3. Sprint Backlog & Kriteria Selesai (Definition of Done - DoD)")
    pdf.paragraph(
        "Untuk memberikan visibilitas estimasi beban kerja kepada tim, berikut adalah daftar Product Backlog Item "
        "(PBI) dengan estimasi bobot Story Points (berdasarkan skala Fibonacci: 1, 2, 3, 5, 8) serta kriteria kelulusannya:"
    )
    
    # Backlog Table
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(243, 244, 246)
    pdf.cell(50, 6, "Product Backlog Item (PBI)", border=1, fill=True)
    pdf.cell(15, 6, "Sprint", border=1, fill=True, align="C")
    pdf.cell(20, 6, "Story Points", border=1, fill=True, align="C")
    pdf.cell(65, 6, "Kriteria Selesai (Definition of Done - DoD)", border=1, fill=True)
    pdf.ln()
    
    pdf.set_font("Helvetica", "", 7)
    backlog_rows = [
        ("Desain UI/UX & Mockup Luxury (Web/Mob)", "Sprint 1", "5", "Seluruh Mockup draf disetujui oleh perwakilan divisi."),
        ("Setup Database USER, ROLE & Otentikasi", "Sprint 1", "8", "Password terenkripsi hash, API login sukses lulus uji unit."),
        ("Form Permintaan Multi-item (Pemohon)", "Sprint 2", "5", "Berhasil menyimpan multi-item & kalkulasi sisa pagu."),
        ("Panel Validasi & Alasan Tolak (Procure)", "Sprint 2", "3", "Notifikasi alasan penolakan terkirim ke unit pemohon."),
        ("Verifikasi Anggaran & Panel PKS", "Sprint 3", "8", "Termin kalkulasi tepat 100%, validasi pagu anggaran unit."),
        ("Panel Tagihan & Kasir Pembayaran", "Sprint 4", "5", "Integrasi pemotongan sisa anggaran riil aman tanpa bug."),
        ("Integrasi Upload Dokumen & Chart.js", "Sprint 5", "5", "Upload file ter-filter tipe & visual grafik analitik valid.")
    ]
    for row in backlog_rows:
        pdf.cell(50, 5.5, row[0], border=1)
        pdf.cell(15, 5.5, row[1], border=1, align="C")
        pdf.cell(20, 5.5, row[2], border=1, align="C")
        pdf.cell(65, 5.5, row[3], border=1)
        pdf.ln()
        
    pdf.output("Tugas_2_Model_SDLC.pdf")
    print("Tugas_2_Model_SDLC.pdf generated.")

# ================= TUGAS 3: ESTIMASI SDM =================
def build_pdf_tugas3():
    pdf = SystemAnalysisPDF(
        document_title="Estimasi Kebutuhan & Manajemen Sumber Daya Manusia",
        doc_code="SIPB-T3-HR"
    )
    pdf.add_page()
    pdf.document_header(subtitle="Tugas 3: Perkiraan Peran Tim Pengembang & Matriks RACI")
    
    pdf.section_heading("1. Manajemen Sumber Daya Proyek")
    pdf.paragraph(
        "Keberhasilan proyek SIPB yang mencakup 3 platform (Web, Android, iOS) dalam durasi 3 bulan sangat bergantung pada "
        "efisiensi komposisi tim. Setiap anggota tim harus memiliki fokus keahlian yang spesifik dan lintas fungsi "
        "untuk menjamin kolaborasi yang sinergis."
    )
    
    pdf.section_heading("2. Kebutuhan Peran Tim Pengembang")
    sdm_desc = "Komposisi tim pengembang yang ramping dan optimal terdiri dari 6 personel kunci."
    if COMPILATION_MODE == 'default':
        sdm_desc += (
            " Struktur pengorganisasian tim ini merujuk pada standar proses rekayasa perangkat lunak "
            "ISO/IEC 29110 untuk organisasi skala kecil (*small entities*) guna menjamin efisiensi alokasi personel."
        )
    pdf.paragraph(sdm_desc)
    pdf.draw_bullet("Bertanggung jawab atas jalannya sprint, koordinasi timeline proyek, manajemen risiko, dan komunikasi sponsor.", "1. Project Manager / Scrum Master:")
    pdf.draw_bullet("Bertanggung jawab merumuskan user stories, merancang skema database (USER, ROLE, transaksi), dan validasi fitur.", "2. System Analyst / Product Owner:")
    pdf.draw_bullet("Bertanggung jawab mendesain antarmuka login & dashboard per peran yang sederhana, bersih, tumpul (soft rounded), dan menggunakan font Inter.", "3. UI/UX Designer:")
    pdf.draw_bullet("Bertanggung jawab membangun antarmuka web responsif dan integrasi dengan API autentikasi maupun transaksi.", "4. Frontend Developer:")
    pdf.draw_bullet("Bertanggung jawab membangun database, API, keamanan hash password (bcrypt), otorisasi token sesi, dan business logic.", "5. Backend Developer:")
    pdf.draw_bullet("Bertanggung jawab menyusun skenario tes, melakukan pengujian fungsional dan keamanan, serta memfasilitasi UAT.", "6. QA Engineer / Software Tester:")
    
    pdf.ln(4)
    pdf.section_heading("3. Matriks Kompetensi Teknologi (Skills Mapping)")
    pdf.paragraph(
        "Untuk memastikan pemilihan personel tim pengembang yang tepat guna, berikut adalah pemetaan "
        "kebutuhan keahlian utama dan teknologi yang digunakan oleh masing-masing peran:"
    )
    
    # Skills Table
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(243, 244, 246)
    pdf.cell(35, 6, "Peran Tim", border=1, fill=True)
    pdf.cell(55, 6, "Keahlian Utama Minimal", border=1, fill=True)
    pdf.cell(60, 6, "Pustaka / Teknologi yang Digunakan", border=1, fill=True)
    pdf.ln()
    
    pdf.set_font("Helvetica", "", 7)
    skill_rows = [
        ("Project Manager", "Manajemen Agile & Risiko", "Jira, Slack, Microsoft Project"),
        ("System Analyst", "Data Modeling & Pembuatan API", "PostgreSQL, DB Diagram, Swagger/OpenAPI"),
        ("UI/UX Designer", "Desain Antarmuka Modern & Bersih", "Figma, Inter Font, Google Material Design"),
        ("Frontend Developer", "Web App Responsif & PWA", "HTML5, CSS Vanilla Flex/Grid, Service Worker"),
        ("Backend Developer", "Keamanan API, Enkripsi, DB Lock", "Node.js, bcrypt, JSON Web Token (JWT)"),
        ("QA Engineer", "Skenario Pengujian Unit & Manual", "Postman, Jest, Selenium")
    ]
    for row in skill_rows:
        pdf.cell(35, 5.5, row[0], border=1)
        pdf.cell(55, 5.5, row[1], border=1)
        pdf.cell(60, 5.5, row[2], border=1)
        pdf.ln()
        
    pdf.ln(4)
    pdf.section_heading("4. Matriks Alokasi Tanggung Jawab (RACI Matrix)")
    pdf.paragraph(
        "Pembagian matriks RACI (R = Responsible, A = Accountable, C = Consulted, I = Informed) "
        "pada modul autentikasi dan alur kerja utama proyek:"
    )
    
    # RACI Table
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(243, 244, 246)
    pdf.cell(50, 6, "Aktivitas Utama Proyek", border=1, fill=True)
    pdf.cell(20, 6, "PM/SM", border=1, fill=True, align="C")
    pdf.cell(20, 6, "Analyst", border=1, fill=True, align="C")
    pdf.cell(20, 6, "UI/UX", border=1, fill=True, align="C")
    pdf.cell(20, 6, "Devs", border=1, fill=True, align="C")
    pdf.cell(20, 6, "QA", border=1, fill=True, align="C")
    pdf.ln()
    
    pdf.set_font("Helvetica", "", 7.5)
    raci_rows = [
        ("Analisis Database USER & RBAC", "C", "A / R", "C", "C", "I"),
        ("Desain UI Login & Navigasi Peran", "I", "C", "A / R", "I", "I"),
        ("Coding Backend Login & Enkripsi", "I", "I", "I", "A / R", "C"),
        ("Integrasi API & Multi-item Flow", "I", "I", "I", "A / R", "C"),
        ("Pengujian Unit Keamanan & UAT", "A", "C", "I", "R (Fix)", "R (Test)")
    ]
    for row in raci_rows:
        pdf.cell(50, 6, row[0], border=1)
        for i in range(1, 6):
            pdf.cell(20, 6, row[i], border=1, align="C")
        pdf.ln()
        
    pdf.output("Tugas_3_Estimasi_SDM.pdf")
    print("Tugas_3_Estimasi_SDM.pdf generated.")

# ================= TUGAS 4: PENJADWALAN TIMELINE =================
def build_pdf_tugas4():
    pdf = SystemAnalysisPDF(
        document_title="Penjadwalan Proyek & Manajemen Waktu",
        doc_code="SIPB-T4-SCH"
    )
    pdf.add_page()
    pdf.document_header(subtitle="Tugas 4: Penjadwalan Kerja & Gantt Chart 3 Bulan")
    
    pdf.section_heading("1. Penjadwalan Waktu Pengembangan")
    pdf.paragraph(
        "Dengan batasan waktu 3 bulan (12 minggu) untuk merilis aplikasi di tiga platform (Web, Android, iOS), "
        "penjadwalan diatur menggunakan time-boxed Sprint. Alokasi Sprint 1 difokuskan pada fondasi autentikasi "
        "dan setup RBAC agar keamanan hak akses data terjamin sejak awal proses pembuatan."
    )
    
    pdf.section_heading("2. Deskripsi Milestone dan Deliverables Sprint")
    pdf.draw_bullet(
        "Analisis database USER, skema login, pembuatan rancangan antarmuka login & dashboard per peran (Web & Mobile layout).",
        "Sprint 1 (Minggu 1-2): Analisis, Login & Desain RBAC"
    )
    pdf.draw_bullet(
        "Coding API autentikasi, enkripsi password, form pengajuan permintaan barang (multi-item) dan menu validasi Procurement.",
        "Sprint 2 (Minggu 3-4): Form Permintaan & Validasi"
    )
    pdf.draw_bullet(
        "Coding modul verifikasi pagu anggaran Budgeting (terhubung sisa pagu unit) dan form draf kontrak PKS Procurement.",
        "Sprint 3 (Minggu 5-6): Alur PKS Kontrak & Budgeting"
    )
    pdf.draw_bullet(
        "Coding modul pencatatan tagihan masuk oleh Keuangan, upload berkas invoice vendor, dan modul pencairan dana kasir.",
        "Sprint 4 (Minggu 7-8): Tagihan Keuangan & Berkas PO"
    )
    pdf.draw_bullet(
        "Penyelesaian modul upload bukti PO, integrasi grafik analitik Chart.js, dan penggabungan sistem multi-platform.",
        "Sprint 5 (Minggu 9-10): Laporan Analitik & Kasir"
    )
    pdf.draw_bullet(
        "Pelaksanaan QA Hardening, uji coba UAT bersama pengguna, perbaikan bug minor, pelatihan, dan deployment produksi.",
        "Sprint 6 (Minggu 11-12): UAT & Rilis Produksi"
    )
    
    pdf.ln(4)
    pdf.section_heading("3. Analisis Beban Kerja Tim Pengembang (Workload Analysis)")
    pdf.paragraph(
        "Untuk memastikan alokasi sumber daya manusia optimal dan mendeteksi adanya kelebihan beban (overload), "
        "dilakukan perhitungan analisis beban kerja (workload) dalam satuan Person-Days per Sprint untuk "
        "tiap personel kunci pengembang. Distribusi beban kerja disusun secara dinamis mengikuti siklus Agile:"
    )
    
    # Workload Table Header
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(243, 244, 246)
    pdf.cell(32, 6, "Peran Tim", border=1, fill=True)
    pdf.cell(16, 6, "Sprint 1", border=1, fill=True, align="C")
    pdf.cell(16, 6, "Sprint 2", border=1, fill=True, align="C")
    pdf.cell(16, 6, "Sprint 3", border=1, fill=True, align="C")
    pdf.cell(16, 6, "Sprint 4", border=1, fill=True, align="C")
    pdf.cell(16, 6, "Sprint 5", border=1, fill=True, align="C")
    pdf.cell(16, 6, "Sprint 6", border=1, fill=True, align="C")
    pdf.cell(22, 6, "Total (MD)", border=1, fill=True, align="C")
    pdf.ln()
    
    pdf.set_font("Helvetica", "", 7.5)
    workload_rows = [
        ("Project Manager / SM", "8 MD", "8 MD", "8 MD", "8 MD", "8 MD", "10 MD", "50 MD"),
        ("System Analyst / PO", "10 MD", "6 MD", "4 MD", "2 MD", "2 MD", "4 MD", "28 MD"),
        ("UI/UX Designer", "10 MD", "6 MD", "4 MD", "2 MD", "2 MD", "2 MD", "26 MD"),
        ("Backend Developer", "6 MD", "8 MD", "10 MD", "8 MD", "8 MD", "6 MD", "46 MD"),
        ("Frontend Developer", "4 MD", "10 MD", "8 MD", "8 MD", "10 MD", "6 MD", "46 MD"),
        ("QA Engineer", "2 MD", "4 MD", "6 MD", "8 MD", "8 MD", "10 MD", "38 MD"),
        ("Total Beban Sprint", "40 MD", "42 MD", "40 MD", "36 MD", "38 MD", "38 MD", "234 MD")
    ]
    for row in workload_rows:
        if row[0] == "Total Beban Sprint":
            pdf.set_font("Helvetica", "B", 7.5)
            pdf.set_fill_color(243, 244, 246)
            fill_opt = True
        else:
            pdf.set_font("Helvetica", "", 7.5)
            fill_opt = False
        pdf.cell(32, 5.5, row[0], border=1, fill=fill_opt)
        for i in range(1, 8):
            pdf.cell(16 if i < 7 else 22, 5.5, row[i], border=1, fill=fill_opt, align="C")
        pdf.ln()
        
    pdf.ln(4)
    pdf.section_heading("4. Analisis Jalur Kritis Proyek (Critical Path Analysis)")
    pdf.paragraph(
        "Berdasarkan ketergantungan antar-tugas pengembangan, draf jalur kritis proyek didefinisikan secara tegas. "
        "Aktivitas pada jalur kritis ini memiliki kelonggaran waktu nol (zero float) sehingga keterlambatan pengerjaan "
        "akan berdampak langsung pada molornya tanggal rilis go-live 3 bulan:"
    )
    
    # Critical Path Table
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(243, 244, 246)
    pdf.cell(50, 6, "Aktivitas Proyek", border=1, fill=True)
    pdf.cell(32, 6, "Prasyarat (Dependency)", border=1, fill=True)
    pdf.cell(23, 6, "Alokasi Waktu", border=1, fill=True, align="C")
    pdf.cell(45, 6, "Status Jalur Proyek", border=1, fill=True)
    pdf.ln()
    
    pdf.set_font("Helvetica", "", 7)
    path_rows = [
        ("Analisis DB USER & Hak Akses", "N/A", "Sprint 1", "JALUR KRITIS (Zero Float)"),
        ("Desain UI Login & Sesi Dashboard", "N/A", "Sprint 1", "JALUR KRITIS (Zero Float)"),
        ("Form Permintaan Multi-item", "Analisis DB USER", "Sprint 2", "JALUR KRITIS (Zero Float)"),
        ("Verifikasi Pagu Anggaran Unit", "Form Permintaan", "Sprint 3", "JALUR KRITIS (Zero Float)"),
        ("Pembuatan PKS & Detail Termin", "Verifikasi Anggaran", "Sprint 3", "JALUR KRITIS (Zero Float)"),
        ("Pencatatan Tagihan Keuangan", "Pembuatan PKS", "Sprint 4", "JALUR KRITIS (Zero Float)"),
        ("Pencairan Kasir & Update Kas", "Pencatatan Tagihan", "Sprint 4", "JALUR KRITIS (Zero Float)"),
        ("UAT Komprehensif & Rilis", "System Integration", "Sprint 6", "JALUR KRITIS (Zero Float)")
    ]
    for row in path_rows:
        pdf.cell(50, 5.5, row[0], border=1)
        pdf.cell(32, 5.5, row[1], border=1)
        pdf.cell(23, 5.5, row[2], border=1, align="C")
        if "KRITIS" in row[3]:
            pdf.set_text_color(185, 28, 28) # Red
            pdf.set_font("Helvetica", "B", 7)
        pdf.cell(45, 5.5, row[3], border=1)
        pdf.ln()
        pdf.set_text_color(55, 65, 81) # reset
        pdf.set_font("Helvetica", "", 7)
        
    pdf.ln(4)
    pdf.section_heading("5. Visualisasi Gantt Chart")
    pdf.add_diagram("gantt.png", w=150)
    pdf.paragraph(
        "Gantt Chart di atas membagi pengerjaan secara berurutan. Sprint 1 bertindak sebagai fondasi utama (Hitam), "
        "diikuti pengembangan modul fungsional (Emas), dan diakhiri dengan tahap stabilisasi UAT dan rilis (Abu-abu)."
    )
    
    pdf.output("Tugas_4_Penjadwalan_Timeline.pdf")
    print("Tugas_4_Penjadwalan_Timeline.pdf generated.")

# ================= TUGAS 5: KEY POINTS PM =================
def build_pdf_tugas5():
    pdf = SystemAnalysisPDF(
        document_title="Laporan Faktor Penentu Kesuksesan Proyek (Critical Success Factors)",
        doc_code="SIPB-T5-KEY"
    )
    pdf.add_page()
    pdf.document_header(subtitle="Tugas 5: Key Points Laporan untuk Project Manager (PM)")
    
    pdf.section_heading("1. Faktor Penentu Kesuksesan Proyek")
    pdf.paragraph(
        "Untuk menjamin Sistem Informasi Pengadaan Barang (SIPB) dapat diselesaikan dalam waktu 3 bulan "
        "pada platform Web, Android, dan iOS dengan kualitas keandalan tinggi, Project Manager harus "
        "memperhatikan Key Points penting dari sisi teknis dan manajerial."
    )
    
    pdf.section_heading("2. Key Points dari Sisi Teknis (Technical Key Points)")
    pdf.draw_bullet(
        "Sistem harus menyimpan password pengguna menggunakan enkripsi hashing satu arah (bcrypt). "
        "Validasi login divalidasi dengan token sesi yang aman baik di sisi klien maupun divalidasi ulang di backend.",
        "Keamanan Autentikasi & Isolasi Peran (RBAC):"
    )
    pdf.draw_bullet(
        "Sistem harus memiliki fungsi validasi aritmatika untuk memastikan akumulasi nominal termin pembayaran "
        "pada kontrak PKS bernilai tepat 100% dari nilai pagu kontrak sebelum disimpan ke database.",
        "Akurasi Kalkulasi Termin Pembayaran:"
    )
    pdf.draw_bullet(
        "Pencairan dana oleh Kasir memotong sisa anggaran unit terkait. Database harus mengadopsi kontrol konkurensi "
        "(transaction locking) untuk mencegah terjadinya race condition apabila terjadi dua proses pencairan dana secara bersamaan.",
        "Kontrol Konkurensi Pengurangan Anggaran:"
    )
    
    pdf.ln(4)
    pdf.section_heading("3. Matriks Manajemen Risiko & Mitigasi (Risk Register Matrix)")
    pdf.paragraph(
        "Sebagai bagian dari manajemen pencegahan kegagalan proyek, berikut adalah daftar register risiko "
        "dari sisi teknis dan manajerial beserta taktik mitigasi otonomnya:"
    )
    
    # Risk Table
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(243, 244, 246)
    pdf.cell(50, 6, "Identifikasi Risiko", border=1, fill=True)
    pdf.cell(16, 6, "Dampak", border=1, fill=True, align="C")
    pdf.cell(18, 6, "Probabilitas", border=1, fill=True, align="C")
    pdf.cell(66, 6, "Strategi Mitigasi / Solusi", border=1, fill=True)
    pdf.ln()
    
    pdf.set_font("Helvetica", "", 7)
    risk_rows = [
        ("Perwakilan divisi lambat melakukan UAT", "Tinggi", "Sedang", "Jadwalkan sesi tes kecil 1 jam pada tiap akhir Sprint Review."),
        ("Session hijacking pada token login", "Kritis", "Rendah", "Terapkan HttpOnly & Secure flags pada cookies penyimpanan token."),
        ("Kesalahan pembulatan termin rupiah", "Sedang", "Tinggi", "Gunakan fungsi pembulatan standar akuntansi di API backend."),
        ("Perubahan kebutuhan di tengah jalan", "Tinggi", "Tinggi", "Terapkan Scope Control ketat; tampung perubahan ke Fase 2."),
        ("Keterlambatan respons invoice supplier", "Tinggi", "Sedang", "PM pastikan adanya kesepakatan SLA respons tertulis dengan vendor.")
    ]
    for row in risk_rows:
        pdf.cell(50, 5.5, row[0], border=1)
        pdf.cell(16, 5.5, row[1], border=1, align="C")
        pdf.cell(18, 5.5, row[2], border=1, align="C")
        pdf.cell(66, 5.5, row[3], border=1)
        pdf.ln()
        
    pdf.ln(4)
    pdf.section_heading("4. Key Points dari Sisi Manajerial (Managerial Key Points)")
    scope_control_text = (
        "Mengingat waktu yang sangat singkat yaitu 3 bulan untuk 3 platform, PM harus menolak tegas permintaan "
        "penambahan fitur di luar modul inti pengadaan (Scope Creep) dan memasukkannya ke rencana pengembangan Fase 2."
    )
    if COMPILATION_MODE == 'default':
        scope_control_text += (
            " Hal ini selaras dengan prinsip tata kelola manajemen keamanan informasi standar ISO/IEC 27001 "
            "untuk mencegah adanya kerentanan keamanan akibat fitur tidak terencana."
        )
    pdf.draw_bullet(
        scope_control_text,
        "Disiplin Pengendalian Ruang Lingkup (Scope Control):"
    )
    pdf.draw_bullet(
        "Alur pengadaan melibatkan aktivitas di luar aplikasi (vendor mengirim barang dan menerbitkan invoice). "
        "Keterlambatan respon vendor luar dapat menghambat kelancaran sistem. PM perlu memastikan adanya kesepakatan SLA "
        "respons yang disetujui secara tertulis dengan vendor.",
        "Mitigasi Ketergantungan Vendor Eksternal (SLA):"
    )
    pdf.draw_bullet(
        "Ada 5 divisi pengguna internal yang terisolasi menu navigasinya. Koordinasi waktu untuk User Acceptance Testing (UAT) "
        "bisa menjadi penghambat rilis. PM wajib mengamankan komitmen waktu uji coba dari perwakilan divisi sejak pertengahan proyek.",
        "Manajemen Komitmen UAT Pengguna:"
    )
    
    pdf.output("Tugas_5_Key_Points_PM.pdf")
    print("Tugas_5_Key_Points_PM.pdf generated.")

if __name__ == "__main__":
    build_pdf_tugas1()
    build_pdf_tugas2()
    build_pdf_tugas3()
    build_pdf_tugas4()
    build_pdf_tugas5()
    print("All PDFs compiled successfully with professional optimization.")
