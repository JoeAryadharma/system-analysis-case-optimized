import os
import sys
from fpdf import FPDF

COMPILATION_MODE = 'optimized' # default
if len(sys.argv) > 1 and sys.argv[1] in ['default', 'optimized']:
    COMPILATION_MODE = sys.argv[1]

class TechnicalDeliveryPDF(FPDF):
    def __init__(self, document_title, doc_code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document_title = document_title
        self.doc_code = doc_code
        self.set_margins(20, 20, 20)
        self.set_auto_page_break(auto=True, margin=20)
        
    def header(self):
        self.set_text_color(31, 41, 55) # Near Black
        self.set_font("Helvetica", "B", 7)
        self.cell(0, 4, f"DOKUMEN RILIS RESMI  |  KODE: {self.doc_code}", new_x="LMARGIN", new_y="NEXT", align="R")
        self.set_font("Times", "I", 8)
        self.cell(0, 4, "TECHNICAL DELIVERY REPORT - JOE ARYADHARMA", new_x="LMARGIN", new_y="NEXT", align="L")
        
        # Gold divider line
        self.set_draw_color(201, 151, 67)
        self.set_line_width(0.5)
        self.line(20, self.get_y() + 2, 190, self.get_y() + 2)
        self.ln(6)

    def footer(self):
        self.set_y(-18)
        self.set_draw_color(229, 231, 235)
        self.set_line_width(0.3)
        self.line(20, self.get_y(), 190, self.get_y())
        
        self.set_text_color(107, 114, 128)
        self.set_font("Helvetica", "I", 7.5)
        self.cell(90, 10, "SIPB TECHNICAL RELEASE - JOE ARYADHARMA CONFIDENTIAL", align="L")
        self.cell(80, 10, f"Halaman {self.page_no()}", align="R")

    def document_header(self, subtitle=""):
        self.set_text_color(31, 41, 55)
        self.set_font("Times", "B", 16)
        self.multi_cell(0, 7, self.document_title, align="L")
        if subtitle:
            self.ln(1)
            self.set_text_color(201, 151, 67)
            self.set_font("Helvetica", "B", 9.5)
            self.cell(0, 5, subtitle.upper(), new_x="LMARGIN", new_y="NEXT", align="L")
        self.ln(4)
        
    def section_heading(self, text):
        self.set_text_color(31, 41, 55)
        self.set_font("Times", "B", 11)
        self.cell(0, 7, text, new_x="LMARGIN", new_y="NEXT", align="L")
        self.set_draw_color(201, 151, 67)
        self.set_line_width(0.5)
        self.line(20, self.get_y(), 60, self.get_y())
        self.ln(2.5)
        
    def paragraph(self, text, style=""):
        self.set_text_color(55, 65, 81)
        if style == "bold":
            self.set_font("Helvetica", "B", 9)
        elif style == "italic":
            self.set_font("Helvetica", "I", 9)
        else:
            self.set_font("Helvetica", "", 9)
        self.multi_cell(0, 4.5, text, align="J")
        self.ln(3)

    def draw_bullet(self, text, bold_prefix=""):
        self.set_text_color(55, 65, 81)
        self.set_font("Helvetica", "", 9)
        self.cell(5, 4.5, chr(149), align="L")
        if bold_prefix:
            self.set_font("Helvetica", "B", 9)
            self.write(4.5, bold_prefix + " ")
            self.set_font("Helvetica", "", 9)
        self.write(4.5, text)
        self.ln(4.5)

def build_delivery_report():
    # Fetch google drive link if exists in env, else use placeholder
    gdrive_link = os.environ.get("GOOGLE_DRIVE_LINK", "https://drive.google.com/drive/folders/1GzUULTWo-zC8a2-08HZZ2V7-4FfcXbdH?usp=sharing")

    pdf = TechnicalDeliveryPDF(
        document_title="Penyerahan Hasil Uji & Solusi Teknis:\nSistem Informasi Pengadaan Barang (SIPB)",
        doc_code="SIPB-TECHNICAL-DELIVERY"
    )
    pdf.add_page()
    pdf.document_header(subtitle="Laporan Penyerahan Resmi (Technical Delivery Report)")
    desc_text = (
        "Dokumen rilis resmi ini disusun oleh Joe Aryadharma untuk menyerahkan seluruh berkas solusi teknis "
        "dan hasil pengujian terhadap studi kasus Sistem Informasi Pengadaan Barang (SIPB). "
        "Proyek ini mencakup pengembangan aplikasi pada platform Web (PWA), Android Native (Jetpack Compose), "
        "dan iOS Native (Swift) dengan mengedepankan keamanan hak akses pengguna berbasis peran (RBAC)"
    )
    if COMPILATION_MODE == 'optimized':
        desc_text += " serta integrasi basis data awan Supabase secara real-time."
    else:
        desc_text += " untuk verifikasi fungsionalitas alur pengadaan."
    pdf.paragraph(desc_text)
    
    pdf.section_heading("1. Tautan Aplikasi Web Live (Vercel Production)")
    pdf.paragraph(
        "Aplikasi web prototipe telah dideploy secara daring pada platform Vercel dan dapat diakses "
        "melalui tautan berikut untuk simulasi pengujian end-to-end:"
    )
    pdf.draw_bullet(
        "https://test-case-system-analysis-case.vercel.app (Alternatif: https://web-app-ashy-nu.vercel.app)",
        "Web App Versi Ter-optimasi (Supabase Cloud):"
    )
    pdf.draw_bullet(
        "https://test-case-system-analysis-case-default.vercel.app (Alternatif: https://prototype-henna-xi.vercel.app)",
        "Web App Versi Default (Offline Demo Mode):"
    )
    pdf.ln(3)

    pdf.section_heading("2. Tautan Repositori Kode Sumber (GitHub)")
    pdf.paragraph(
        "Seluruh repositori GitHub disetel dalam visibilitas publik untuk memudahkan peninjauan kode sumber "
        "serta struktur arsitektur sistem oleh tim evaluator perusahaan:"
    )
    pdf.draw_bullet(
        "https://github.com/JoeAryadharma/system-analysis-case-optimized",
        "Repositori Proyek Ter-optimasi (Optimized):"
    )
    pdf.draw_bullet(
        "https://github.com/JoeAryadharma/system-analysis-case-default",
        "Repositori Dokumen Standar (Default):"
    )
    pdf.draw_bullet(
        "https://github.com/JoeAryadharma/system-analysis-case-sipb",
        "Repositori Master Integrasi (All-in-One):"
    )
    pdf.ln(3)

    pdf.section_heading("3. Tautan Folder Penyimpanan Laporan & File Biner (Google Drive)")
    pdf.paragraph(
        "Untuk kemudahan pengunduhan berkas dokumen laporan Tugas 1-5 format PDF, diagram alir sistem (High-Res), "
        "skema SQL, serta file biner aplikasi Android (sipb-mobile.apk), silakan akses tautan Google Drive berikut:"
    )
    pdf.draw_bullet(
        gdrive_link,
        "Google Drive Folder:"
    )
    pdf.ln(3)

    if COMPILATION_MODE == 'optimized':
        pdf.section_heading("4. Ringkasan Peningkatan & Optimasi Sistem")
        pdf.paragraph(
            "Sistem SIPB versi Optimized telah dibekali dengan berbagai penyempurnaan taktis:"
        )
        pdf.draw_bullet(
            "Mengintegrasikan client-side SDK Supabase untuk sinkronisasi database awan secara real-time pada 5 peran pengguna.",
            "Integrasi Supabase Cloud:"
        )
        pdf.draw_bullet(
            "Mengganti popup alert() browser dengan modal dialog kustom yang dilengkapi animasi mikro fade-in dan ikon visual yang estetis.",
            "Kustom Dialog Alert & UX:"
        )
        pdf.draw_bullet(
            "Menampilkan format rupiah ter-lokalisasi secara live di bawah input estimasi anggaran (Budgeting) dan denda potongan kasir.",
            "Nominal Currency Helper:"
        )
        pdf.draw_bullet(
            "Menyertakan analisis RACI matrix, estimasi Story Points, peta jalur kritis pengembangan, operational risk register, dan audit keamanan eksternal.",
            "Laporan Analisis Taktis:"
        )
        pdf.ln(4)
    else:
        pdf.ln(2)
    
    # Sign-off section
    pdf.set_text_color(31, 41, 55)
    pdf.set_font("Times", "B", 10)
    pdf.cell(100, 5, "Hormat Saya,", new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.ln(12)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.cell(100, 4, "Joe Aryadharma", new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.set_font("Helvetica", "", 8.5)
    pdf.cell(100, 4, "Kandidat System Analyst & Developer", new_x="LMARGIN", new_y="NEXT", align="L")

    pdf.output("Laporan_Penyerahan_Hasil_Uji_SIPB.pdf")
    print("Laporan_Penyerahan_Hasil_Uji_SIPB.pdf generated successfully.")

if __name__ == "__main__":
    build_delivery_report()
