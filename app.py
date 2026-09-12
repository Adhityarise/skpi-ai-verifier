import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import os
from dotenv import load_dotenv

# 1. Load API Key secara tersembunyi dari file .env (Backend Server)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="SKPI AI Verifier Portal", layout="wide")

st.title("🎓 Portal Layanan SKPI Mahasiswa")
st.caption("Sistem Pengajuan & Verifikasi Otomatis Dokumen SKPI Berbasis AI")

# Sidebar
with st.sidebar:
    st.header("📌 Informasi Layanan SKPI")
    st.info("""
    **Ketentuan Unggah Berkas:**
    - Pastikan gambar sertifikat/surat keterangan jelas (tidak buram).
    - Nama pada dokumen wajib sesuai dengan nama mahasiswa.
    - Sertifikat Magang wajib mencantumkan **durasi jam kerja**.
    - Sertifikat Keahlian wajib mencantumkan **skor/nilai** dan **tanda tangan penerbit**.
    """)
    st.caption("🤖 Powered by Adhtyarise")

# UI Form Utama Mahasiswa
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Form Pengajuan Dokumen")
    student_name = st.text_input("Nama Lengkap Mahasiswa:", "Adhitya")
    student_nim = st.text_input("NIM:", "2024001001")
    uploaded_file = st.file_uploader("Upload Bukti Dokumen (JPG/PNG):", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Preview Dokumen Mahasiswa", use_container_width=True)

with col2:
    st.subheader("2. Status Verifikasi Dokumen Anda")
    
    if uploaded_file and st.button("🚀 Ajukan & Verifikasi Dokumen", type="primary"):
        # Pengecekan API Key backend tersembunyi
        if not api_key:
            st.error("⚠️ Sistem Backend Error: Kunci API server belum terkonfigurasi di file .env!")
        else:
            with st.spinner("Sistem AI sedang mengevaluasi regulasi dokumen Anda..."):
                try:
                    # Inisialisasi API Key dari backend
                    genai.configure(api_key=api_key)
                    
                    system_instruction = f"""
                    <system_prompt>
                      <context>
                        Anda adalah sistem AI Verifikator SKPI otomatis untuk perguruan tinggi. 
                        Tugas Anda adalah memvalidasi dokumen mahasiswa berdasarkan regulasi kampus.
                      </context>

                      <kategori_kegiatan>
                        1. PRESTASI_DAN_PENGHARGAAN:
                           - Pemenang Lomba (Juara I, II, III, Harapan I, II, ) minimal tingkat Kampus (Seni, Agama, Literatur, Sains/IT).
                           - Pemateri/Narasumber workshop minimal tingkat Kabupaten.
                           - Penulis Buku, HAKI, atau Penelitian Dosen.
                        
                        2. KEIKUTSERTAAN_ORGANISASI:
                           - Internal (DPM, BEM, Hima) atau Eksternal Kampus.

                        3. SERTIFIKAT_KEAHLIAN:
                           - Bahasa Asing (TOEFL/IELTS/TOEC), Keahlian Akademik (IT, Akuntansi), Non-Akademik.
                           * Syarat Wajib: Harus ada Nama, Lembaga Penerbit, Tanggal, Hasil/Nilai, serta Nama & TTD Pejabat Penerbit.

                        4. KERJA_PRAKTIK_MAGANG:
                           - Magang Lembaga/Instansi, Pertukaran Pelajar.
                           * Syarat Wajib: HARUS mencantumkan durasi kegiatan (contoh: 160 jam).
                      </kategori_kegiatan>

                      <instructions>
                        1. Analisis gambar dokumen. Identifikasi kategori (1, 2, 3, atau 4).
                        2. Cocokkan Nama Penerima dengan: '{student_name}'.
                        3. Periksa Syarat Wajib Khusus:
                           - Jika KERJA_PRAKTIK_MAGANG: pastikan ada durasi jam. Jika tidak ada, wajib MANUAL_REVIEW.
                           - Jika SERTIFIKAT_KEAHLIAN: pastikan ada Nilai/Skor dan TTD Pejabat.
                        4. Tentukan status: AUTO_APPROVE (jika nama cocok, gambar jelas, syarat terpenuhi) atau MANUAL_REVIEW.
                      </instructions>
                    </system_prompt>
                    """

                    model = genai.GenerativeModel(
                        model_name="gemini-3.5-flash-lite",
                        system_instruction=system_instruction,
                        generation_config={"response_mime_type": "application/json"}
                    )

                    user_prompt = f"""
                    Verifikasi dokumen ini untuk mahasiswa bernama: {student_name}.
                    Keluarkan output JSON persis seperti ini:
                    {{
                        "is_name_matched": boolean,
                        "confidence_score": float (0.00 - 1.00),
                        "category": "PRESTASI_DAN_PENGHARGAAN | KEIKUTSERTAAN_ORGANISASI | SERTIFIKAT_KEAHLIAN | KERJA_PRAKTIK_MAGANG",
                        "extracted_data": {{
                            "recipient_name": "string",
                            "activity_title": "string",
                            "issuing_institution": "string",
                            "issue_date": "string",
                            "rank_or_role": "string",
                            "duration_hours": "string atau null",
                            "score_or_grade": "string atau null"
                        }},
                        "status": "AUTO_APPROVE | MANUAL_REVIEW",
                        "flag_reason": "string atau null"
                    }}
                    """

                    response = model.generate_content([image, user_prompt])
                    res_json = json.loads(response.text)
                    
                    if res_json["status"] == "AUTO_APPROVE":
                        st.success(f"✅ DOKUMEN DISERTAKAN KE SKPI (Confidence Score: {res_json['confidence_score']*100:.1f}%)")
                    else:
                        st.warning(f"⚠️ BERKAS DIALIKAN KE VERIFIKASI MANUAL ADMIN (Confidence Score: {res_json['confidence_score']*100:.1f}%)")
                        st.caption(f"📌 Catatan AI: {res_json.get('flag_reason', 'Dokumen memerlukan tinjauan manual admin')}")

                    st.write("**Hasil Audit & Ekstraksi AI:**")
                    st.json(res_json)

                except Exception as e:
                    st.error(f"Terjadi kesalahan pada server AI: {str(e)}")