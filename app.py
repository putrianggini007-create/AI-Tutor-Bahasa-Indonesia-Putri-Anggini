import streamlit as st
import os
import re
from collections import Counter

# =========================================================
# TAMPILAN / WARNA SAJA
# =========================================================

st.markdown("""
<style>

    /* ================================
       WARNA DASAR HALAMAN
       ================================ */

    .stApp {
        background: linear-gradient(
            135deg,
            #fff7fb 0%,
            #f8f3ff 45%,
            #f2f9ff 100%
        );
    }

    /* Area utama */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(
            135deg,
            #fff8fb 0%,
            #f9f4ff 50%,
            #f3faff 100%
        );
    }

    /* ================================
       HEADER STREAMLIT
       ================================ */

    [data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.75);
    }

    /* ================================
       SIDEBAR
       ================================ */

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #f9e8f1 0%,
            #eee8fa 50%,
            #e8f3fa 100%
        );
    }

    [data-testid="stSidebar"] * {
        color: #4f4657;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #6d4f72;
    }

    /* ================================
       JUDUL
       ================================ */

    h1 {
        color: #5d4865 !important;
    }

    h2 {
        color: #66516d !important;
    }

    h3 {
        color: #705a77 !important;
    }

    p {
        color: #5f5863;
    }

    /* ================================
       TEXT AREA
       ================================ */

    [data-testid="stTextArea"] textarea {
        background-color: rgba(255, 255, 255, 0.92) !important;
        color: #4d4652 !important;
        border: 2px solid #ead8e8 !important;
        border-radius: 16px !important;
        padding: 14px !important;
        box-shadow: 0 4px 15px rgba(120, 90, 130, 0.08);
    }

    [data-testid="stTextArea"] textarea:focus {
        border: 2px solid #cba9d2 !important;
        box-shadow: 0 0 0 3px rgba(203, 169, 210, 0.18) !important;
    }

    [data-testid="stTextArea"] textarea::placeholder {
        color: #aaa0ae !important;
    }

    /* ================================
       TOMBOL
       ================================ */

    .stButton > button {
        background: linear-gradient(
            135deg,
            #dca9c7,
            #b9a7d8
        ) !important;

        color: white !important;
        border: none !important;
        border-radius: 14px !important;

        padding: 12px 20px !important;

        font-weight: 600 !important;
        font-size: 15px !important;

        box-shadow: 0 5px 15px rgba(150, 120, 160, 0.20);

        transition: all 0.25s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(
            135deg,
            #c997b8,
            #a796c7
        ) !important;

        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(150, 120, 160, 0.25);
    }

    /* ================================
       INFO / SUCCESS / WARNING / ERROR
       ================================ */

    [data-testid="stAlert"] {
        border-radius: 14px !important;
        border: none !important;
    }

    /* ================================
       KARTU INFO
       ================================ */

    [data-testid="stAlert"][kind="info"] {
        background: #f3ecfa !important;
    }

    /* ================================
       EXPANDER
       ================================ */

    [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.75);
        border: 1px solid #eadfec !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 15px rgba(120, 100, 130, 0.06);
    }

    [data-testid="stExpander"] summary {
        color: #66516d !important;
        font-weight: 600;
    }

    /* ================================
       CODE / NAMA FOLDER
       ================================ */

    code {
        background-color: #f1eaf5 !important;
        color: #71577a !important;
        border-radius: 8px;
    }

    /* ================================
       GARIS PEMBATAS
       ================================ */

    hr {
        border: none !important;
        height: 1px !important;

        background: linear-gradient(
            90deg,
            transparent,
            #dbc8dc,
            transparent
        ) !important;

        margin: 25px 0 !important;
    }

    /* ================================
       METRIK STREAMLIT
       ================================ */

    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid #eadfeb;
        border-radius: 16px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(120, 100, 130, 0.07);
    }

    [data-testid="stMetricLabel"] {
        color: #817485 !important;
    }

    [data-testid="stMetricValue"] {
        color: #67506e !important;
    }

    /* ================================
       FOOTER
       ================================ */

    footer {
        color: #8c8190 !important;
    }

</style>
""", unsafe_allow_html=True)
# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="AI Tutor Bahasa Indonesia Putri Anggini",
    page_icon="📚",
    layout="wide"
)


# =========================================================
# KONFIGURASI DATABASE
# =========================================================

FOLDER_DATABASE = "database"


# =========================================================
# FUNGSI MEMBACA DATABASE TXT
# =========================================================

def baca_database():

    data = []

    if not os.path.exists(FOLDER_DATABASE):
        os.makedirs(FOLDER_DATABASE)

    daftar_file = os.listdir(FOLDER_DATABASE)

    for nama_file in daftar_file:

        if nama_file.lower().endswith(".txt"):

            lokasi_file = os.path.join(
                FOLDER_DATABASE,
                nama_file
            )

            try:

                with open(
                    lokasi_file,
                    "r",
                    encoding="utf-8"
                ) as file:

                    isi = file.read()

                data.append({
                    "nama_file": nama_file,
                    "isi": isi
                })

            except Exception as error:

                st.error(
                    f"Gagal membaca {nama_file}: {error}"
                )

    return data


# =========================================================
# MEMBERSIHKAN TEKS
# =========================================================

def bersihkan_teks(teks):

    teks = teks.lower()

    teks = re.sub(
        r"[^a-zA-ZÀ-ÿ0-9\s]",
        " ",
        teks
    )

    teks = re.sub(
        r"\s+",
        " ",
        teks
    )

    return teks.strip()


# =========================================================
# STOPWORDS SEDERHANA
# =========================================================

STOPWORDS = {
    "yang",
    "dan",
    "di",
    "ke",
    "dari",
    "pada",
    "dengan",
    "untuk",
    "dalam",
    "adalah",
    "itu",
    "ini",
    "atau",
    "apa",
    "bagaimana",
    "mengapa",
    "sebutkan",
    "jelaskan",
    "jelaskanlah",
    "tentang",
    "suatu",
    "sebuah",
    "secara",
    "merupakan",
    "dapat",
    "akan",
    "sebagai",
    "oleh",
    "lebih",
    "juga",
    "tidak",
    "tersebut"
}


# =========================================================
# MENGAMBIL KATA KUNCI
# =========================================================

def ambil_kata_kunci(pertanyaan):

    teks = bersihkan_teks(pertanyaan)

    kata = teks.split()

    kata_kunci = []

    for item in kata:

        if len(item) > 2 and item not in STOPWORDS:

            kata_kunci.append(item)

    return kata_kunci


# =========================================================
# SISTEM PENILAIAN RELEVANSI
# =========================================================

def hitung_relevansi(pertanyaan, isi):

    kata_kunci = ambil_kata_kunci(pertanyaan)

    if len(kata_kunci) == 0:
        return 0

    teks_database = bersihkan_teks(isi)

    kata_database = teks_database.split()

    frekuensi = Counter(kata_database)

    skor = 0

    for kata in kata_kunci:

        if kata in frekuensi:

            jumlah = frekuensi[kata]

            if jumlah > 10:
                jumlah = 10

            skor += jumlah

    # Bonus jika frasa pertanyaan muncul
    pertanyaan_bersih = bersihkan_teks(
        pertanyaan
    )

    if pertanyaan_bersih in teks_database:

        skor += 20

    # Bonus jika kata kunci utama terdapat di judul
    baris_awal = teks_database[:500]

    for kata in kata_kunci:

        if kata in baris_awal:

            skor += 5

    return skor


# =========================================================
# MENCARI MATERI
# =========================================================

def cari_materi(pertanyaan, database):

    hasil = []

    for data in database:

        skor = hitung_relevansi(
            pertanyaan,
            data["isi"]
        )

        if skor > 0:

            hasil.append({
                "nama_file": data["nama_file"],
                "isi": data["isi"],
                "skor": skor
            })

    hasil.sort(
        key=lambda x: x["skor"],
        reverse=True
    )

    return hasil


# =========================================================
# MEMBUAT POTONGAN MATERI
# =========================================================

def ambil_potongan_relevan(
    pertanyaan,
    isi,
    jumlah_maksimal=1200
):

    kata_kunci = ambil_kata_kunci(
        pertanyaan
    )

    paragraf = re.split(
        r"\n\s*\n|\r\n",
        isi
    )

    paragraf_relevan = []

    for p in paragraf:

        p_bersih = bersihkan_teks(p)

        skor = 0

        for kata in kata_kunci:

            if kata in p_bersih:

                skor += 1

        if skor > 0:

            paragraf_relevan.append(
                (skor, p.strip())
            )

    paragraf_relevan.sort(
        key=lambda x: x[0],
        reverse=True
    )

    hasil = ""

    for skor, p in paragraf_relevan:

        if len(hasil) + len(p) <= jumlah_maksimal:

            hasil += p + "\n\n"

    if hasil.strip() == "":

        hasil = isi[:jumlah_maksimal]

    return hasil.strip()


# =========================================================
# LOAD DATABASE
# =========================================================

database = baca_database()


# =========================================================
# HEADER APLIKASI
# =========================================================

st.title("📚 AI Tutor Bahasa Indonesia Putri Anggini")

st.write(
    "Sistem pembelajaran berbasis Python, "
    "Streamlit, dan Knowledge Base TXT."
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📖 Knowledge Base")

    st.write(
        "Database dibaca otomatis dari folder:"
    )

    st.code("database/")

    st.write(
        f"Jumlah file database: **{len(database)}**"
    )

    st.divider()

    if len(database) > 0:

        st.subheader("Materi tersedia")

        for data in database:

            nama = data["nama_file"]

            nama = nama.replace(
                ".txt",
                ""
            )

            nama = nama.replace(
                "_",
                " "
            )

            st.write(
                "📄 " + nama.title()
            )

    else:

        st.warning(
            "Belum ada file TXT di folder database."
        )


# =========================================================
# FORM PERTANYAAN
# =========================================================

st.subheader("💬 Tanyakan Sesuatu")

pertanyaan = st.text_area(
    "Masukkan pertanyaan Anda:",
    placeholder=(
        "Contoh: Apa yang dimaksud "
        "dengan kalimat efektif?"
    ),
    height=120
)


# =========================================================
# TOMBOL TANYAKAN
# =========================================================

tombol = st.button(
    "🔍 TANYAKAN",
    use_container_width=True
)


# =========================================================
# PROSES PERTANYAAN
# =========================================================

if tombol:

    if pertanyaan.strip() == "":

        st.warning(
            "Silakan masukkan pertanyaan terlebih dahulu."
        )

    elif len(database) == 0:

        st.error(
            "Database TXT belum ditemukan."
        )

    else:

        with st.spinner(
            "Sedang mencari materi..."
        ):

            hasil = cari_materi(
                pertanyaan,
                database
            )


        # =================================================
        # JIKA MATERI DITEMUKAN
        # =================================================

        if len(hasil) > 0:

            hasil_utama = hasil[0]

            st.success(
                "Materi yang paling relevan ditemukan."
            )

            st.subheader(
                "💡 Jawaban"
            )

            jawaban = ambil_potongan_relevan(
                pertanyaan,
                hasil_utama["isi"]
            )

            st.info(jawaban)


            # =============================================
            # SUMBER MATERI
            # =============================================

            st.subheader(
                "📚 Sumber Materi"
            )

            nama_file = hasil_utama[
                "nama_file"
            ]

            st.write(
                f"**{nama_file}**"
            )


            # =============================================
            # MATERI TERKAIT
            # =============================================

            if len(hasil) > 1:

                st.subheader(
                    "📑 Materi Terkait"
                )

                for item in hasil[1:4]:

                    with st.expander(
                        item["nama_file"]
                    ):

                        potongan = (
                            ambil_potongan_relevan(
                                pertanyaan,
                                item["isi"],
                                800
                            )
                        )

                        st.write(
                            potongan
                        )


        # =================================================
        # JIKA TIDAK DITEMUKAN
        # =================================================

        else:

            st.warning(
                "Maaf, materi yang Anda tanyakan "
                "belum ditemukan dalam database."
            )

            st.write(
                "Coba gunakan kata kunci yang "
                "lebih spesifik."
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AI Tutor Bahasa Indonesia | "
    "Python + Streamlit + TXT Knowledge Base"
)