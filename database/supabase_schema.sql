-- =========================================================================
-- SKEMA BASIS DATA SUPABASE - SISTEM INFORMASI PENGADAAN BARANG (SIPB)
-- VERSION: 2.0
-- =========================================================================

-- 1. Tabel Pagu Anggaran Unit (budget_limits)
CREATE TABLE IF NOT EXISTS budget_limits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    unit VARCHAR(100) UNIQUE NOT NULL,
    pagu_awal NUMERIC(15, 2) NOT NULL,
    sisa_pagu NUMERIC(15, 2) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE budget_limits ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read-write" ON budget_limits FOR ALL USING (true) WITH CHECK (true);

-- 2. Tabel Pengajuan Permintaan Utama (permintaan)
CREATE TABLE IF NOT EXISTS permintaan (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    unit VARCHAR(100) NOT NULL,
    tanggal DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING_PROCUREMENT',
    alasan TEXT,
    estimasi_biaya NUMERIC(15, 2) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE permintaan ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read-write" ON permintaan FOR ALL USING (true) WITH CHECK (true);

-- 3. Tabel Detail Item Pengajuan (permintaan_items)
CREATE TABLE IF NOT EXISTS permintaan_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    permintaan_id UUID REFERENCES permintaan(id) ON DELETE CASCADE NOT NULL,
    nama VARCHAR(255) NOT NULL,
    qty INTEGER NOT NULL CHECK (qty > 0),
    satuan VARCHAR(50) NOT NULL
);

ALTER TABLE permintaan_items ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read-write" ON permintaan_items FOR ALL USING (true) WITH CHECK (true);

-- 4. Tabel Kontrak PKS (pks_kontrak)
CREATE TABLE IF NOT EXISTS pks_kontrak (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    permintaan_id UUID REFERENCES permintaan(id) ON DELETE RESTRICT UNIQUE NOT NULL,
    no_kontrak VARCHAR(100) UNIQUE NOT NULL,
    no_draft_po VARCHAR(100),
    no_po VARCHAR(100) UNIQUE NOT NULL,
    tanggal_kontrak DATE NOT NULL DEFAULT CURRENT_DATE,
    nama_vendor VARCHAR(100) NOT NULL DEFAULT 'Supplier Utama',
    total_harga NUMERIC(15, 2) NOT NULL,
    po_file_path VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE pks_kontrak ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read-write" ON pks_kontrak FOR ALL USING (true) WITH CHECK (true);

-- 4a. Tabel Detail Item PKS (pks_items)
CREATE TABLE IF NOT EXISTS pks_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pks_id UUID REFERENCES pks_kontrak(id) ON DELETE CASCADE NOT NULL,
    nama_barang VARCHAR(255) NOT NULL,
    jumlah INTEGER NOT NULL CHECK (jumlah > 0),
    satuan VARCHAR(50) NOT NULL,
    harga_satuan NUMERIC(15, 2) NOT NULL,
    potongan_harga NUMERIC(15, 2) NOT NULL DEFAULT 0,
    harga_total NUMERIC(15, 2) NOT NULL
);

ALTER TABLE pks_items ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read-write" ON pks_items FOR ALL USING (true) WITH CHECK (true);

-- 5. Tabel Skema Termin Pembayaran (pks_termins)
CREATE TABLE IF NOT EXISTS pks_termins (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pks_id UUID REFERENCES pks_kontrak(id) ON DELETE CASCADE NOT NULL,
    termin_index INTEGER NOT NULL,
    persen NUMERIC(5, 2) NOT NULL CHECK (persen > 0 AND persen <= 100),
    nominal NUMERIC(15, 2) NOT NULL,
    tanggal_pembayaran DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING_BILLING',
    UNIQUE (pks_id, termin_index)
);

ALTER TABLE pks_termins ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read-write" ON pks_termins FOR ALL USING (true) WITH CHECK (true);

-- 6. Tabel Tagihan Vendor (tagihan)
CREATE TABLE IF NOT EXISTS tagihan (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pks_id UUID REFERENCES pks_kontrak(id) ON DELETE RESTRICT NOT NULL,
    termin_id UUID REFERENCES pks_termins(id) ON DELETE RESTRICT UNIQUE NOT NULL,
    unit VARCHAR(100) NOT NULL,
    no_invoice VARCHAR(100) UNIQUE NOT NULL,
    nominal NUMERIC(15, 2) NOT NULL,
    invoice_file_path VARCHAR(255) NOT NULL,
    tanggal_tagihan DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(50) NOT NULL DEFAULT 'INVOICE_RECORDED',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE tagihan ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read-write" ON tagihan FOR ALL USING (true) WITH CHECK (true);

-- 6a. Tabel Detail Item Tagihan (tagihan_items)
CREATE TABLE IF NOT EXISTS tagihan_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tagihan_id UUID REFERENCES tagihan(id) ON DELETE CASCADE NOT NULL,
    nama_barang VARCHAR(255) NOT NULL,
    jumlah INTEGER NOT NULL CHECK (jumlah > 0),
    satuan VARCHAR(50) NOT NULL,
    harga_satuan NUMERIC(15, 2) NOT NULL,
    potongan_harga NUMERIC(15, 2) NOT NULL DEFAULT 0,
    harga_total NUMERIC(15, 2) NOT NULL
);

ALTER TABLE tagihan_items ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read-write" ON tagihan_items FOR ALL USING (true) WITH CHECK (true);

-- 7. Tabel Catatan Buku Kas (bukukas)
CREATE TABLE IF NOT EXISTS bukukas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tanggal DATE NOT NULL DEFAULT CURRENT_DATE,
    unit VARCHAR(100) NOT NULL,
    no_invoice VARCHAR(100) NOT NULL,
    nominal_pembayaran NUMERIC(15, 2) NOT NULL,
    denda NUMERIC(15, 2) NOT NULL DEFAULT 0,
    nominal_final NUMERIC(15, 2) NOT NULL,
    tipe VARCHAR(50) NOT NULL DEFAULT 'DEBET',
    tanggal_pembayaran DATE NOT NULL DEFAULT CURRENT_DATE,
    nominal_pembayaran_sebelum_potongan NUMERIC(15, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE bukukas ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read-write" ON bukukas FOR ALL USING (true) WITH CHECK (true);

-- 8. Data Inisiasi Awal Pagu Anggaran
INSERT INTO budget_limits (unit, pagu_awal, sisa_pagu) VALUES
('IT & Infrastructure', 500000000.00, 425000000.00),
('Operational Support', 300000000.00, 275000000.00),
('Human Resources', 200000000.00, 185000000.00),
('Marketing & Sales', 400000000.00, 385000000.00)
ON CONFLICT (unit) DO UPDATE 
SET pagu_awal = EXCLUDED.pagu_awal, sisa_pagu = EXCLUDED.sisa_pagu;
