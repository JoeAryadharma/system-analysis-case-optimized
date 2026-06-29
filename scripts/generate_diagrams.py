import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set standard styles to Inter-like sans-serif
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Inter', 'DejaVu Sans', 'Arial', 'Helvetica']

def draw_usecase():
    fig, ax = plt.subplots(figsize=(10, 8.5), dpi=150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # System boundary box
    system_box = patches.Rectangle((2.5, 0.5), 5, 9, linewidth=1.5, edgecolor='#4b5563', facecolor='#f9fafb', zorder=1)
    ax.add_patch(system_box)
    ax.text(5, 9.2, "Sistem Pengadaan Barang (SIPB)", ha='center', va='bottom', fontsize=12, fontweight='bold', color='#111827')
    
    # Actors
    actors = [
        ("Unit Pemohon", 1, 8),
        ("Petugas Procurement", 1, 5),
        ("Petugas Budgeting", 1, 2),
        ("Petugas Keuangan", 9, 6.5),
        ("Kasir", 9, 3.5)
    ]
    
    actor_coords = {}
    for name, x, y in actors:
        # Draw simple stick figure
        head = patches.Circle((x, y), 0.25, facecolor='#ffffff', edgecolor='#4b5563', linewidth=1.5, zorder=3)
        ax.add_patch(head)
        ax.plot([x, x], [y-0.25, y-0.9], color='#4b5563', linewidth=1.5, zorder=3)
        ax.plot([x-0.4, x+0.4], [y-0.5, y-0.5], color='#4b5563', linewidth=1.5, zorder=3)
        ax.plot([x, x-0.3], [y-0.9, y-1.4], color='#4b5563', linewidth=1.5, zorder=3)
        ax.plot([x, x+0.3], [y-0.9, y-1.4], color='#4b5563', linewidth=1.5, zorder=3)
        ax.text(x, y-1.8, name, ha='center', va='top', fontsize=9, fontweight='bold', color='#1f2937')
        actor_coords[name] = (x, y-0.5)
        
    # Use cases
    use_cases = [
        ("UC0: Autentikasi Login", (5, 8.4)),
        ("UC1: Mengajukan Permintaan", (5, 7.3)),
        ("UC2: Validasi Permintaan", (5, 6.2)),
        ("UC3: Verifikasi Anggaran", (5, 5.1)),
        ("UC4: Membuat PKS Kontrak", (5, 4.0)),
        ("UC5: Upload Bukti PO", (5, 2.9)),
        ("UC6: Mencatat Tagihan", (5, 1.8)),
        ("UC7: Pencairan Dana Kasir", (5, 0.8))
    ]
    
    uc_coords = {}
    for uc_id, (x, y) in use_cases:
        ellipse = patches.Ellipse((x, y), 2.2, 0.65, facecolor='#ffffff', edgecolor='#4b5563', linewidth=1.2, zorder=2)
        ax.add_patch(ellipse)
        ax.text(x, y, uc_id, ha='center', va='center', fontsize=8, fontweight='medium', color='#111827')
        uc_coords[uc_id.split(":")[0]] = (x, y)
        
    # Draw connections (lines)
    connections = [
        ("Unit Pemohon", "UC0"),
        ("Petugas Procurement", "UC0"),
        ("Petugas Budgeting", "UC0"),
        ("Petugas Keuangan", "UC0"),
        ("Kasir", "UC0"),
        ("Unit Pemohon", "UC1"),
        ("Petugas Procurement", "UC2"),
        ("Petugas Budgeting", "UC3"),
        ("Petugas Procurement", "UC4"),
        ("Petugas Procurement", "UC5"),
        ("Petugas Keuangan", "UC6"),
        ("Kasir", "UC7")
    ]
    
    for actor_name, uc_key in connections:
        ax_x, ax_y = actor_coords[actor_name]
        uc_x, uc_y = uc_coords[uc_key]
        
        start_x = ax_x + 0.4 if ax_x < 5 else ax_x - 0.4
        end_x = uc_x - 1.1 if ax_x < 5 else uc_x + 1.1
        
        ax.plot([start_x, end_x], [ax_y, uc_y], color='#9ca3af', linestyle='-', linewidth=0.9, zorder=1)
        
    plt.title("Use Case Diagram - Sistem Pengadaan Barang (SIPB)", fontsize=13, fontweight='bold', pad=20, color='#111827')
    plt.tight_layout()
    plt.savefig("usecase.png", bbox_inches='tight', dpi=150)
    plt.close()
    print("usecase.png generated.")

def draw_flowchart():
    fig, ax = plt.subplots(figsize=(10, 11), dpi=150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # helper for drawing shapes
    def draw_box(text, x, y, w, h, box_type="proc"):
        if box_type == "start":
            box = patches.FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.1", facecolor='#f3f4f6', edgecolor='#4b5563', linewidth=1.5)
        elif box_type == "decision":
            pts = np.array([[x, y+h/2], [x+w/2, y], [x, y-h/2], [x-w/2, y]])
            box = patches.Polygon(pts, facecolor='#ffffff', edgecolor='#d97706', linewidth=1.5)
        else: # process
            box = patches.Rectangle((x-w/2, y-h/2), w, h, facecolor='#ffffff', edgecolor='#4b5563', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='medium', color='#111827')
        
    # Nodes layout
    draw_box("Mulai", 5, 10.6, 1.2, 0.3, "start")
    draw_box("Halaman Login: Input Username & Password", 5, 9.9, 3.8, 0.45)
    draw_box("Kredensial Valid?", 5, 8.9, 2.2, 0.7, "decision")
    
    # Rejection / Failure paths
    draw_box("Notifikasi Kredensial Salah", 1.8, 8.9, 2.5, 0.5)
    
    # Success path & Role Routing
    draw_box("Identifikasi Peran & Otorisasi Menu (RBAC)", 5, 7.8, 4.0, 0.5)
    draw_box("Unit Pemohon Input Permintaan\n(Multi-item: Tanggal, Nama, Qty, Satuan)", 5, 6.9, 3.8, 0.5)
    draw_box("Procurement Validasi?", 5, 5.9, 2.2, 0.7, "decision")
    
    # Procurement Rejection
    draw_box("Procurement Input Alasan Penolakan\n& Notifikasi ke Pemohon", 1.8, 5.9, 2.8, 0.5)
    
    # Budgeting verification
    draw_box("Budgeting Verifikasi Anggaran?", 5, 4.8, 2.4, 0.7, "decision")
    draw_box("Budgeting Input Alasan Penolakan\n& Notifikasi ke Pemohon", 1.8, 4.8, 2.8, 0.5)
    
    # Workflow Downstream
    draw_box("Procurement Buat PKS & Upload PO\n(Input: No Kontrak, PO, Detail Harga, Termin)", 5, 3.7, 4.0, 0.55)
    draw_box("Keuangan Input Tagihan & Upload Invoice\n(Input: Tgl Tagihan, PO, Rincian, Potongan)", 5, 2.7, 4.0, 0.55)
    draw_box("Kasir Cairkan Dana & Update Buku Kas\n(Input: Tgl Pembayaran, Denda, Nominal Final)", 5, 1.7, 4.0, 0.55)
    draw_box("Selesai (Kas Transaksi Lunas)", 5, 0.8, 2.2, 0.35, "start")
    
    # Draw arrows
    arrow_style = dict(arrowstyle="->", lw=1.2, color='#4b5563')
    
    ax.annotate("", xy=(5, 10.15), xytext=(5, 10.45), arrowprops=arrow_style)
    ax.annotate("", xy=(5, 9.25), xytext=(5, 9.65), arrowprops=arrow_style)
    
    # Login decision
    ax.annotate("", xy=(3.05, 8.9), xytext=(3.9, 8.9), arrowprops=arrow_style)
    ax.text(3.45, 9.0, "Tidak", ha='center', va='bottom', fontsize=7.5, color='#dc2626')
    ax.annotate("", xy=(5, 8.05), xytext=(5, 8.55), arrowprops=arrow_style)
    ax.text(5.1, 8.3, "Ya", ha='left', va='center', fontsize=7.5, color='#16a34a')
    
    # Connect Failure back to Login
    ax.annotate("", xy=(5, 9.9), xytext=(1.8, 9.15), arrowprops=arrow_style)
    
    # From Role Routing to Input
    ax.annotate("", xy=(5, 7.15), xytext=(5, 7.55), arrowprops=arrow_style)
    ax.annotate("", xy=(5, 6.25), xytext=(5, 6.65), arrowprops=arrow_style)
    
    # Procurement Decision
    ax.annotate("", xy=(3.2, 5.9), xytext=(3.9, 5.9), arrowprops=arrow_style)
    ax.text(3.5, 6.0, "Tolak", ha='center', va='bottom', fontsize=7.5, color='#dc2626')
    ax.annotate("", xy=(5, 5.15), xytext=(5, 5.55), arrowprops=arrow_style)
    ax.text(5.1, 5.35, "Setuju", ha='left', va='center', fontsize=7.5, color='#16a34a')
    
    # Budgeting Decision
    ax.annotate("", xy=(3.2, 4.8), xytext=(3.8, 4.8), arrowprops=arrow_style)
    ax.text(3.5, 4.9, "Tolak", ha='center', va='bottom', fontsize=7.5, color='#dc2626')
    ax.annotate("", xy=(5, 4.0), xytext=(5, 4.45), arrowprops=arrow_style)
    ax.text(5.1, 4.2, "Setuju", ha='left', va='center', fontsize=7.5, color='#16a34a')
    
    # Downstream lines
    ax.annotate("", xy=(5, 3.0), xytext=(5, 3.4), arrowprops=arrow_style)
    ax.annotate("", xy=(5, 2.0), xytext=(5, 2.4), arrowprops=arrow_style)
    ax.annotate("", xy=(5, 1.0), xytext=(5, 1.4), arrowprops=arrow_style)
    
    # Connect rejection lines to Selesai (Rejection)
    ax.plot([0.3, 0.3], [5.9, 0.8], color='#4b5563', linestyle='--', linewidth=1.0)
    ax.plot([1.8, 0.3], [5.9, 5.9], color='#4b5563', linestyle='--', linewidth=1.0)
    ax.plot([1.8, 0.3], [4.8, 4.8], color='#4b5563', linestyle='--', linewidth=1.0)
    ax.annotate("", xy=(3.9, 0.8), xytext=(0.3, 0.8), arrowprops=arrow_style)
    
    plt.title("Flowchart Alur Fungsional & Navigasi Peran (RBAC)", fontsize=13, fontweight='bold', pad=15, color='#111827')
    plt.tight_layout()
    plt.savefig("flowchart.png", bbox_inches='tight', dpi=150)
    plt.close()
    print("flowchart.png generated.")

def draw_erd():
    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    def draw_entity(title, attributes, x, y, w, h):
        ax.add_patch(patches.Rectangle((x, y+h-0.35), w, 0.35, facecolor='#f3f4f6', edgecolor='#4b5563', linewidth=1.2))
        ax.text(x+w/2, y+h-0.18, title, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#111827')
        ax.add_patch(patches.Rectangle((x, y), w, h-0.35, facecolor='#ffffff', edgecolor='#4b5563', linewidth=1.2))
        attr_text = "\n".join(attributes)
        ax.text(x+0.1, y+h-0.45, attr_text, ha='left', va='top', fontsize=7.5, color='#374151', linespacing=1.3)

    # Entities with RBAC tables
    draw_entity("ROLE", ["id_role (PK)", "nama_role"], 0.2, 5.6, 1.8, 1.2)
    draw_entity("USER", ["id_user (PK)", "username (UK)", "password_hash", "nama_lengkap", "id_role (FK)"], 0.2, 3.2, 1.8, 1.6)
    draw_entity("UNIT", ["id_unit (PK)", "nama_unit", "pagu_anggaran", "sisa_anggaran"], 0.2, 0.8, 1.8, 1.6)
    
    draw_entity("PERMINTAAN", ["id_permintaan (PK)", "tanggal_pengajuan", "id_unit (FK)", "id_user_pemohon (FK)", "status"], 2.8, 3.0, 2.2, 1.8)
    draw_entity("ITEM_PERMINTAAN", ["id_item_perm (PK)", "id_permintaan (FK)", "nama_barang", "jumlah", "satuan"], 5.8, 5.5, 2.2, 1.7)
    
    draw_entity("PKS (KONTRAK)", ["id_pks (PK)", "nomor_kontrak (UK)", "nomor_po_supp", "tanggal_kontrak", "bukti_po_path", "id_permintaan (FK)"], 5.8, 2.8, 2.2, 1.9)
    draw_entity("TERMIN_BAYAR", ["id_termin (PK)", "id_pks (FK)", "tanggal_bayar", "persen", "nominal"], 8.5, 4.8, 1.4, 1.5)
    draw_entity("TAGIHAN (INVOICE)", ["id_tagihan (PK)", "no_tagihan_vendor", "no_po", "tanggal_tagihan", "id_pks (FK)"], 8.5, 2.6, 1.4, 1.7)
    draw_entity("PEMBAYARAN_KASIR", ["id_pembayaran (PK)", "id_tagihan (FK)", "tanggal_bayar", "total_bayar"], 8.5, 0.5, 1.4, 1.5)

    # Draw Relation Lines with cardinality notation
    def draw_relation(p1, p2, text=""):
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#9ca3af', linestyle='-', linewidth=0.9)
        if text:
            mx, my = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
            ax.text(mx, my+0.05, text, ha='center', va='bottom', fontsize=7, color='#4b5563')

    # ROLE -- USER (1 - N)
    draw_relation((1.1, 5.6), (1.1, 4.8), "1 : N")
    # USER -- PERMINTAAN (1 - N)
    draw_relation((2.0, 4.0), (2.8, 4.0), "1 : N")
    # UNIT -- PERMINTAAN (1 - N)
    draw_relation((1.1, 2.4), (2.8, 3.2), "1 : N")
    # PERMINTAAN -- ITEM_PERMINTAAN (1 - N)
    draw_relation((5.0, 4.5), (5.8, 6.0), "1 : N")
    # PERMINTAAN -- PKS (1 - 1)
    draw_relation((5.0, 3.8), (5.8, 3.6), "1 : 1")
    # PKS -- TERMIN_BAYAR (1 - N)
    draw_relation((8.0, 3.9), (8.5, 5.0), "1 : N")
    # PKS -- TAGIHAN (1 - N)
    draw_relation((8.0, 3.5), (8.5, 3.3), "1 : N")
    # TAGIHAN -- PEMBAYARAN_KASIR (1 - 1)
    draw_relation((9.2, 2.6), (9.2, 2.0), "1 : 1")

    plt.title("Entity Relation Diagram (ERD) - Manajemen Data & Keamanan RBAC", fontsize=13, fontweight='bold', pad=15, color='#111827')
    plt.tight_layout()
    plt.savefig("erd.png", bbox_inches='tight', dpi=150)
    plt.close()
    print("erd.png generated.")

def draw_sequence():
    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    participants = [
        ("Pengguna", 1.2),
        ("Antarmuka (UI)", 3.2),
        ("Sistem / Controller", 5.7),
        ("Database USER", 8.2)
    ]
    
    # Draw vertical lifelines
    for name, x in participants:
        ax.plot([x, x], [1, 9], color='#9ca3af', linestyle='--', linewidth=1)
        ax.add_patch(patches.Rectangle((x-0.9, 9.0), 1.8, 0.45, facecolor='#f3f4f6', edgecolor='#4b5563', linewidth=1.2, zorder=2))
        ax.text(x, 9.2, name, ha='center', va='center', fontsize=8, fontweight='bold', color='#1f2937')
        
    # Sequence arrows (Autentikasi Login & Sesi)
    sequence = [
        (8.0, 1.2, 3.2, "1. Input Username & Password"),
        (7.0, 3.2, 5.7, "2. Kirim Kredensial (POST /login)"),
        (6.0, 5.7, 8.2, "3. Query User & Validasi Password"),
        (5.0, 8.2, 5.7, "4. Return Data User & Role (FK)"),
        (4.0, 5.7, 5.7, "5. Generate Sesi / Token Otorisasi"),
        (3.0, 5.7, 3.2, "6. Redirect ke Dashboard Peran (RBAC)"),
        (2.0, 3.2, 1.2, "7. Render Halaman Menu Spesifik Peran")
    ]
    
    arrow_style = dict(arrowstyle="->", lw=1.1, color='#111827')
    
    for y, x_from, x_to, msg in sequence:
        if x_from == x_to:
            ax.plot([x_from, x_from+0.4, x_from+0.4, x_from], [y+0.2, y+0.2, y-0.2, y-0.2], color='#111827', linewidth=1.1)
            ax.text(x_from+0.5, y, msg, ha='left', va='center', fontsize=7.5, color='#1f2937')
        else:
            ax.annotate("", xy=(x_to, y), xytext=(x_from, y), arrowprops=arrow_style)
            ax.text((x_from+x_to)/2, y+0.1, msg, ha='center', va='bottom', fontsize=7.5, color='#1f2937')
        
    plt.title("UML Sequence Diagram - Autentikasi Login & Otorisasi Sesi", fontsize=13, fontweight='bold', pad=15, color='#111827')
    plt.tight_layout()
    plt.savefig("sequence.png", bbox_inches='tight', dpi=150)
    plt.close()
    print("sequence.png generated.")

def draw_gantt():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    
    tasks = [
        "Sprint 6: UAT & Rilis Produksi",
        "Sprint 5: Laporan Analitik & Kasir",
        "Sprint 4: Tagihan Keuangan & Berkas PO",
        "Sprint 3: Alur PKS Kontrak & Budgeting",
        "Sprint 2: Form Permintaan & Validasi",
        "Sprint 1: Analisis, Login & Desain RBAC"
    ]
    
    starts = [10, 8, 6, 4, 2, 0] # in weeks
    durations = [2, 2, 2, 2, 2, 2] # in weeks
    
    colors = ['#9ca3af', '#d97706', '#d97706', '#d97706', '#d97706', '#1f2937']
    
    bars = ax.barh(tasks, durations, left=starts, height=0.5, color=colors, edgecolor='#4b5563', linewidth=1)
    
    workloads = [
        "38 MD (QA & Release)",
        "38 MD (Chart & Kasir)",
        "36 MD (Invoice & PO)",
        "40 MD (PKS & Budget)",
        "42 MD (Form & Validate)",
        "40 MD (Auth & RBAC)"
    ]
    
    for bar, workload in zip(bars, workloads):
        width = bar.get_width()
        x = bar.get_x()
        y = bar.get_y()
        ax.text(x + width + 0.15, y, workload, ha='left', va='center', fontsize=8.5, color='#1f2937', fontweight='bold')
        
    ax.set_xlabel("Waktu (Minggu ke-)", fontsize=9, fontweight='medium', color='#1f2937')
    ax.set_xlim(-0.5, 15.5)
    ax.set_xticks(range(0, 13, 2))
    ax.grid(axis='x', linestyle=':', color='#9ca3af', alpha=0.6)
    
    legend_elements = [
        patches.Patch(facecolor='#1f2937', edgecolor='#4b5563', label='Inisiasi, Login & RBAC Desain'),
        patches.Patch(facecolor='#d97706', edgecolor='#4b5563', label='Pengembangan Alur Bisnis'),
        patches.Patch(facecolor='#9ca3af', edgecolor='#4b5563', label='Stabilisasi & UAT')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=8)
    
    plt.title("Penjadwalan Gantt Chart (Timeline 3 Bulan)", fontsize=12, fontweight='bold', pad=15, color='#111827')
    plt.tight_layout()
    plt.savefig("gantt.png", bbox_inches='tight', dpi=150)
    plt.close()
    print("gantt.png generated.")

if __name__ == "__main__":
    draw_usecase()
    draw_flowchart()
    draw_erd()
    draw_sequence()
    draw_gantt()
    print("All updated diagrams generated successfully.")
